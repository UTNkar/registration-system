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
    InterestCheck, EmailConfirmations, RiverraftingTeam, ImportantDate
)
from registrationSystem.utils import send_win_email, is_utn_member
from registrationSystem.forms import (
    InterestCheckForm, CreateAccountForm, RiverraftingUserForm,
    RiverraftingTeamForm
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
    print(person_nr, password)
    user = authenticate(request, username=person_nr, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('overview'))
    else:
        return redirect(settings.LOGIN_URL)


def register(request):
    if request.POST:
        form = InterestCheckForm(request.POST)

        if form.is_valid():
            interest_check_obj, _ = InterestCheck.objects.get_or_create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                person_nr=form.cleaned_data['person_nr']
            )

            status = interest_check_obj.status

            if status == "mail unconfirmed":
                confirmation = EmailConfirmations.objects.create(
                    interestCheckId=interest_check_obj
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
        form = InterestCheckForm()
    return render(request, "register_page.html", {'form': form})


def status(request):
    interest_check_id = request.session.get('interest_check_id', None)
    interest_check_obj = InterestCheck.objects.get(id=interest_check_id)

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
    group_model = RiverraftingTeam
    user_id = request.user.id

    user = user_model.objects.get(id=user_id)
    group = user.belongs_to_group

    if not group:
        raise Http404('There is no group associated to this user.')

    is_leader = group.leader.id == user.id

    UserFormSet = modelformset_factory(
        user_model,
        form=RiverraftingUserForm,
        extra=0
    )
    GroupFormSet = modelformset_factory(
        group_model,
        form=RiverraftingTeamForm,
        max_num=1
    )

    # TODO: Don't use the RiverraftingUserForm, but rather choose form
    # depending on what user model is selected.
    my_form = RiverraftingUserForm(instance=user)
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
            my_form = RiverraftingUserForm(request.POST, instance=user)

            if my_form.is_valid():
                my_form.save()

    return render(request,
                  "overview.html",
                  {
                      "me": my_form,
                      "group_name": group.name,
                      "group_nr": group.number,
                      "others": others_formset,
                      "group": group_formset,
                      "is_leader": is_leader,
                      "dates": dates,
                  })


def change_status(request):
    interest_check_id = request.session.get('interest_check_id', None)
    interest_check_obj = InterestCheck.objects.get(id=interest_check_id)

    if interest_check_obj.status == "won":
        interest_check_obj.status = "accepted"
    elif interest_check_obj.status == "lost":
        interest_check_obj.status = "waiting"

    interest_check_obj.save()
    return redirect(reverse('status'))


def activate(request, token):
    try:
        confirmation = EmailConfirmations.objects.get(pk=token)
        user = confirmation.interestCheckId
        user.status = 'waiting'
        confirmation.delete()
        user.save()
        return redirect(reverse('status'))
    except(InterestCheck.DoesNotExist):
        return HttpResponse('Activation link is invalid!')


def temp_set_to_won(request, uid):
    # Temporary dev view. Remove this when there is functionality
    # to change winner's status to 'won'.
    # Allows changing of user's status with button press.

    user = get_object_or_404(InterestCheck, id=uid)

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
    connector = get_object_or_404(EmailConfirmations, id=uid)
    user = connector.interestCheckId

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

        # Keep the InterestCheck (user) with status 'confirmed'
        # for statistical purposes.
        user.status = "confirmed"
        user.save()

        # Delete the EmailConfirmations. The randomized token
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
