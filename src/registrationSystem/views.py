from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.forms import modelformset_factory
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from registrationSystem.models import (
    RaffleEntry, EmailConfirmation, RiverRaftingTeam
)
from registrationSystem.utils import send_win_email, is_utn_member
from registrationSystem.forms import (
    RaffleEntryForm, CreateAccountForm, RiverRaftingUserForm,
    RiverRaftingTeamForm
)
from django.conf import settings


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
        return redirect(settings.LOGIN_URL)


def register(request):
    if request.POST:
        form = RaffleEntryForm(request.POST)

        if form.is_valid():
            interest_check_obj, _ = RaffleEntry.objects.get_or_create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                person_nr=form.cleaned_data['person_nr']
            )

            status = interest_check_obj.status

            if status == "mail unconfirmed":
                confirmation = EmailConfirmation.objects.create(
                    raffleEntryId=interest_check_obj
                )
                confirmation.save()

                message = render_to_string(
                    'email/confirm_email.html',
                    {
                        'name': interest_check_obj.name,
                        'domain': 'localhost:8000',
                        'token': confirmation.id,
                    }
                )
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    'Activate your account', message, to=[to_email]
                )

                email.send()

            request.session['interest_check_id'] = interest_check_obj.id

            interest_check_obj.status = "won"

            interest_check_obj.save()
            return redirect(reverse('status'))
    else:
        form = RaffleEntryForm()
    return render(request, "register_page.html", {'form': form})


def status(request):
    interest_check_id = request.session.get('interest_check_id', None)
    interest_check_obj = RaffleEntry.objects.get(id=interest_check_id)

    if interest_check_obj.status == "mail unconfirmed":
        template = "mail_unconfirmed.html"
    elif interest_check_obj.status == "waiting":
        template = "waiting.html"
    elif interest_check_obj.status == "won":
        template = "won.html"
    elif interest_check_obj.status == "lost":
        template = "lost.html"
    elif interest_check_obj.status == "accepted":
        template = "accepted.html"
    elif interest_check_obj.status == "declined":
        template = "declined.html"

    return render(request,
                  "status/" + template,
                  {"interest_check_obj": interest_check_obj})


@login_required
def overview(request, id=None):
    user_model = get_user_model()
    group_model = RiverRaftingTeam
    user_id = request.user.id

    user = user_model.objects.get(id=user_id)
    group = user.belongs_to_group

    if not group:
        raise Http404('There is no group associated to this user.')

    UserFormSet = modelformset_factory(user_model, form=RiverRaftingUserForm)
    GroupFormSet = modelformset_factory(
        group_model, form=RiverRaftingTeamForm, max_num=1)
    user_formset = UserFormSet(queryset=user_model.objects.filter(
        belongs_to_group=user.belongs_to_group.id))
    group_formset = GroupFormSet(
        queryset=group_model.objects.filter(id=user.belongs_to_group.id))

    if request.method == "POST":
        if request.POST['type'] == 'group':
            group_formset = GroupFormSet(
                request.POST, queryset=group_model.objects.filter(
                    id=user.belongs_to_group.id
                ))
            if group_formset.is_valid():
                group_formset.save()
        else:
            user_formset = UserFormSet(
                request.POST,
                queryset=user_model.objects.filter(
                    belongs_to_group=user.belongs_to_group.id))
            if user_formset.is_valid():
                user_formset.save()

    return render(request,
                  "overview.html",
                  {
                      "group_name": group.name,
                      "group_nr": group.number,
                      "users": user_formset,
                      "group": group_formset
                  })


def change_status(request):
    interest_check_id = request.session.get('interest_check_id', None)
    interest_check_obj = RaffleEntry.objects.get(id=interest_check_id)

    if interest_check_obj.status == "won":
        interest_check_obj.status = "accepted"
    elif interest_check_obj.status == "lost":
        interest_check_obj.status = "waiting"

    interest_check_obj.save()
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


def temp_set_to_won(request, uid):
    # Temporary dev view. Remove this when there is functionality
    # to change winner's status to 'won'.
    # Allows changing of user's status with button press.

    user = get_object_or_404(RaffleEntry, id=uid)

    if request.method == "POST":
        user.status = 'won'
        user.save()
        send_win_email(user)

    context = {
        'name': user.name,
        'status': user.status,
        'uid': uid
    }
    return render(request, 'registrationSystem/temp_set-to-won.html', context)


def create_account(request, uid):
    connector = get_object_or_404(EmailConfirmation, id=uid)
    user = connector.raffleEntryId

    if request.method == "POST":
        form = CreateAccountForm(request.POST)
    else:
        form = CreateAccountForm(initial={
            'name': user.name,
            'person_nr': user.person_nr,
            'email': user.email
        })

    if form.is_valid():
        phone_nr = form.cleaned_data['phone_nr']
        password = form.cleaned_data['password']
        # There is no need to encrypt the password here, the user manager
        # handles that in the database.
        get_user_model().objects.create(
            name=user.name,
            email=user.email,
            person_nr=user.person_nr,
            phone_nr=phone_nr,
            password=password,
            is_utn_member=is_utn_member(user.person_nr)
        )

        # Keep the RaffleEntry (user) with status 'confirmed'
        # for statistical purposes.
        user.status = "confirmed"
        user.save()

        # Delete the EmailConfirmation. The randomized token
        # should only be used once!
        connector.delete()
        return HttpResponseRedirect('/temp/')

    context = {
        'uid': uid,
        'form': form
    }
    return render(request, 'registrationSystem/create_account.html', context)


def temp(request):
    return render(request, 'registrationSystem/temp.html')