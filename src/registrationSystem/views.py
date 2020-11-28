from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    Http404,
    HttpResponseForbidden
)
from django.urls import reverse
from django.forms import modelformset_factory
from django.contrib.auth import get_user_model
from registrationSystem.models import (
    RaffleEntry, EmailConfirmation, RiverRaftingTeam, ImportantDate
)
from registrationSystem.utn_pay import get_payment_link
from registrationSystem.utils import user_has_won, send_email, is_utn_member
from registrationSystem.forms import (
    RaffleEntryForm, CreateGroupForm, JoinGroupForm, RiverRaftingUserForm,
    RiverRaftingTeamForm
)


@login_required
def make_payment(request):
    team = request.user.belongs_to_group

    if not request.user.is_team_leader():
        return HttpResponseForbidden()

    # Only allow one payment
    if team.payment_initialized:
        return HttpResponseForbidden()

    payment_link = get_payment_link(request.user)

    team.payment_initialized = True
    team.save()

    return redirect(payment_link)


def sign_in(request):
    current_user = request.user
    if current_user.is_authenticated:
        return redirect(reverse('overview'))
    else:
        return render(request, "login_page.html")


def login_user(request):
    person_nr = request.POST.get('person_nr')
    password = request.POST.get("password")
    user = authenticate(request, username=person_nr, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('overview'))
    else:
        # TODO: Send show nice failed to login page
        return HttpResponse('Unauthorized', status=401)


def register(request):
    if request.POST:
        form = RaffleEntryForm(request.POST)
        if form.is_valid():
            raffle_entry, created = form.save()

            if created:
                send_email(raffle_entry, request.get_host())

            # Update cookie. Used when changing accounts or 'logging' back in
            request.session['raffle_entry_id'] = raffle_entry.id

            return redirect(reverse('status'))
    else:
        form = RaffleEntryForm()
    return render(request, "register_page.html", {'form': form})


def status(request):
    raffle_entry_id = request.session['raffle_entry_id']
    raffle_entry_obj = RaffleEntry.objects.get(id=raffle_entry_id)
    status = raffle_entry_obj.status

    if status == "mail unconfirmed":
        template = "mail_unconfirmed.html"
    elif status == "waiting":
        template = "waiting.html"
    elif status == "won":
        template = "won.html"
    elif status == "lost":
        template = "lost.html"
    elif status == "accepted":
        template = "accepted.html"
    elif status == "declined":
        template = "declined.html"
    elif status == "confirmed":
        template = "confirmed.html"

    return render(request,
                  "status/" + template,
                  {"raffle_entry_obj": raffle_entry_obj})


@login_required
def overview(request, id=None):
    user_model = get_user_model()
    group_model = RiverRaftingTeam
    user_id = request.user.id

    user = user_model.objects.get(id=user_id)
    group = user.belongs_to_group

    if not group:
        raise Http404('There is no group associated to this user.')

    is_leader = group.leader.id == user.id
    UserFormSet = modelformset_factory(
        user_model,
        form=RiverRaftingUserForm,
        extra=0
    )
    GroupFormSet = modelformset_factory(
        group_model,
        form=RiverRaftingTeamForm,
        max_num=1
    )

    # TODO: Don't use the RiverraftingUserForm, but rather choose form
    # depending on what user model is selected.
    my_form = RiverRaftingUserForm(instance=user)
    others_formset = UserFormSet(
        queryset=user_model.objects.filter(
            belongs_to_group=user.belongs_to_group.id).exclude(id=user_id),
    )

    group_formset = GroupFormSet(
        queryset=group_model.objects.filter(id=user.belongs_to_group.id))
    dates = ImportantDate.objects.all()

    if request.method == "POST":
        if request.POST['type'] == 'group':
            group_formset = GroupFormSet(
                request.POST, queryset=group_model.objects.filter(
                    id=user.belongs_to_group.id
                ))
            if group_formset.is_valid():
                group_formset.save()
        elif request.POST['type'] == 'others':
            others_formset = UserFormSet(
                request.POST,
                queryset=user_model.objects.filter(
                    belongs_to_group=user.belongs_to_group.id).exclude(
                        id=user_id
                    ))

            if others_formset.is_valid():
                others_formset.save()
        else:
            my_form = RiverRaftingUserForm(request.POST, instance=user)

            if my_form.is_valid():
                my_form.save()

    context = {
        "me": my_form,
        "group_name": group.name,
        "group_nr": group.number,
        "others": others_formset,
        "group": group_formset,
        "is_leader": is_leader,
        "dates": dates,
    }
    if is_leader:
        context["join_id"] = group.join_id

    return render(request, "overview.html", context)


# TODO: Remove this view when status can be changed from the admin pages
def change_status(request):
    # If the user loses and wants to re-enter the raffle, of
    # if the user wins and wants their spot.
    raffle_entry_id = request.session['raffle_entry_id']
    raffle_entry_obj = RaffleEntry.objects.get(id=raffle_entry_id)

    if raffle_entry_obj.status == "won":
        user_has_won(raffle_entry_obj, request.get_host())
        raffle_entry_obj.status = "accepted"
    elif raffle_entry_obj.status == "lost":
        raffle_entry_obj.status = "waiting"

    raffle_entry_obj.save()
    return redirect(reverse('status'))


def activate(request, token):
    try:
        confirmation = EmailConfirmation.objects.get(pk=token)
        user = confirmation.raffleEntryId
        user.status = 'waiting'
        confirmation.delete()
        user.save()
        return redirect(reverse('status'))
    except(RaffleEntry.DoesNotExist):
        return HttpResponse('Activation link is invalid!')


def create_group(request, email_confirm_id):
    connector = get_object_or_404(
        EmailConfirmation,
        id=email_confirm_id
    )
    user = connector.raffleEntryId

    if(request.method == "POST"):
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            # There is no need to encrypt the password here, the user manager
            # handles that in the database. Just make sure to use create_user()
            leader = get_user_model().objects.create_user(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                person_nr=form.cleaned_data["person_nr"],
                phone_nr=form.cleaned_data["phone_nr"],
                password=form.cleaned_data["password"],
                is_utn_member=is_utn_member(form.cleaned_data["person_nr"]),
            )

            # Create a new group and assign it to the user
            group = RiverRaftingTeam.objects.create(leader=leader)

            leader.belongs_to_group = group
            leader.save()

            # Keep the RaffleEntry (user) with status 'confirmed'
            # for statistical purposes.
            user.status = "confirmed"
            user.save()

            # Delete the EmailConfirmation. The randomized token
            # should only be used once!
            connector.delete()
            return HttpResponseRedirect(reverse('status'))
    else:
        form = CreateGroupForm(initial={
            'name': user.name,
            'person_nr': user.person_nr,
            'email': user.email
        })

    context = {
        'form': form,
    }
    # TODO: Replace with working link
    return render(request, 'registrationSystem/create_group.html', context)


def join_group(request, group_join_id):
    # Create a new account (without a previously existing
    # raffle entry) and join an already existing group.
    group = get_object_or_404(RiverRaftingTeam, join_id=group_join_id)

    if request.method == "POST":
        form = JoinGroupForm(request.POST, group=group)
        if form.is_valid():
            # There is no need to encrypt the password here, the user manager
            # handles that in the database.
            get_user_model().objects.create_user(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                person_nr=form.cleaned_data["person_nr"],
                phone_nr=form.cleaned_data["phone_nr"],
                password=form.cleaned_data["password"],
                is_utn_member=is_utn_member(form.cleaned_data["person_nr"]),
                belongs_to_group=group
            )

            return HttpResponseRedirect(reverse('overview'))
    else:
        form = JoinGroupForm(group=group)

    context = {
        'form': form,
        'group': group,
    }
    return render(request, 'registrationSystem/join_group.html', context)
