from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from registrationSystem.models import (
    InterestCheck, RiverraftingUser, EmailConfirmations
)
from registrationSystem.forms import InterestCheckForm, CreateAccountForm
from registrationSystem.utils import send_win_email


def start(request):
    if request.POST:
        form = InterestCheckForm(request.POST)

        if form.is_valid():
            interest_check_obj, _ = InterestCheck.objects.get_or_create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                person_nr=form.cleaned_data['person_nr'],
                status=form.cleaned_data['status']
            )
            status = form.cleaned_data['status']
            if not status:
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
            return redirect(reverse('status'))
    else:
        form = InterestCheckForm(initial={'status': 'Mail-Unconfirmed'})

    return render(request, "start_page.html", {'form': form})


def status(request):
    interest_check_id = request.session['interest_check_id']
    interest_check_obj = InterestCheck.objects.get(id=interest_check_id)
    return render(request,
                  "status_page.html",
                  {"interest_check_obj": interest_check_obj})


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
        RiverraftingUser.objects.create(name=user.name,
                                        email=user.email,
                                        person_nr=user.person_nr,
                                        phone_nr=phone_nr,
                                        password=password,
                                        is_utn_member=True)

        user.status = "confirmed"
        user.save()
        # Keep the InterestCheck (user) with status 'confirmed'
        # for statistical purposes.

        connector.delete()
        # Delete the EmailConfirmations. The randomized token
        # should only be used once!
        return HttpResponseRedirect('/temp/')

    context = {
        'uid': uid,
        'form': form
    }
    return render(request, 'registrationSystem/create_account.html', context)


def temp(request):
    return render(request, 'registrationSystem/temp.html')
