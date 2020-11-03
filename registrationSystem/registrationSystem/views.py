from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from registrationSystem.models import InterestCheck, EmailConfirmations
from registrationSystem.forms import InterestCheckForm


def sign_in(request):
    current_user = request.user
    if current_user.is_authenticated:
        return redirect('/raft_info')
    else:
        return render(request, "login_page.html")


def login_user(request):
    uname = request.POST.get('username')
    passw = request.POST.get("pass")
    user = authenticate(request, username=uname, password=passw)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return redirect('/raft_info')


@login_required
def raft_info(request):
    return render(request, "raft_info.html")


def register(request):
    if request.POST:
        form = InterestCheckForm(request.POST)

        # fråga om detta
        if form.is_valid():
            interest_check_obj, _ = InterestCheck.objects.get_or_create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                person_nr=form.cleaned_data['person_nr']
            )

            status = interest_check_obj.status

            if status == "mail unconfirmed":                         # fråga om detta
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

            # These three rows are not supposed to be here later
            interest_check_obj.status = "won"
            interest_check_obj.save()
            print(interest_check_obj.status)

            return redirect(reverse('status'))
    else:
        form = InterestCheckForm()
    return render(request, "register_page.html", {'form': form})


def status(request):
    interest_check_id = request.session['interest_check_id']
    interest_check_obj = InterestCheck.objects.get(id=interest_check_id)

    print(interest_check_obj.status)

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


def accepted(request):
    interest_check_id = request.session['interest_check_id']
    interest_check_obj = InterestCheck.objects.get(id=interest_check_id)

    interest_check_obj.status = "accepted"
    interest_check_obj.save()

    return redirect(reverse('status'))


def reapply(request):
    interest_check_id = request.session['interest_check_id']
    interest_check_obj = InterestCheck.objects.get(id=interest_check_id)

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
