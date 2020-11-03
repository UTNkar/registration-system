from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from registrationSystem.models import InterestCheck, Group, User, RiverraftingUser, get_group_model
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

def overview(request):
    user_model = get_user_model()
    group_model = get_group_model()
    user_id = 2 # temp

    if request.method == 'POST':
        user_id = request.user.id

        req = request.POST.copy()

        del req['csrfmiddlewaretoken']

        user_model.objects.update_or_create(id=user_id, defaults=req)

    user = user_model.objects.get(id=user_id)
    group = group_model.objects.get(id=user.belongs_to_group.id)
    others = user_model.objects.filter(belongs_to_group=group.id).exclude(id=user_id)

    return render(request,
                  "overview.html",
                  { "user": user,
                    "group": group,
                    "others": others, })

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
