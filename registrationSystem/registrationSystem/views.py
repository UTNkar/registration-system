from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from registrationSystem.models import InterestCheck, EmailConfirmations
from registrationSystem.forms import InterestCheckForm


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
                'Derp', message, to=[to_email]
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
        # TODO Set user status to active?
        user.status = 'waiting'
        confirmation.delete()
        user.save()
        return redirect(reverse('status'))
    except(InterestCheck.DoesNotExist):
        return HttpResponse('Activation link is invalid!')
