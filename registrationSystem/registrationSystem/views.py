from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from registrationSystem.models import InterestCheck, Group, User, RiverraftingUser, get_group_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from registrationSystem.models import (
    InterestCheck, RiverraftingUser, EmailConfirmations
)
from registrationSystem.forms import InterestCheckForm, CreateAccountForm

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
        req = request.POST.copy()
        del req['csrfmiddlewaretoken']
        req_type = req['type']

        # todo: check that people aren't trying to edit
        # unique properties to things that already exist
        if req_type == 'group':
            group_model.objects.update_or_create(id=req['id'], defaults=req)
        elif req_type == 'user':
            user_model.objects.update_or_create(id=req['id'], defaults=req)
        else:
            pass # Error management here

    user = user_model.objects.get(id=user_id)
    group = group_model.objects.get(id=user.belongs_to_group.id)
    everyone = user_model.objects.filter(belongs_to_group=group.id)

    return render(request,
                  "overview.html",
                  { "user": user,
                    "group": group,
                    "others": everyone.exclude(id=user_id),
                    "all": everyone})

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


def create_account(request, uid):
    user = get_object_or_404(InterestCheck, id=uid)

    if request.method == "POST":
        form = CreateAccountForm(request.POST)
    else:
        form = CreateAccountForm(initial={
            'name': user.name,
            'person_nr': user.person_nr,
            'email': user.email
        })

    if form.is_valid():
        password = form.cleaned_data['password']
        # There is no need to encrypt the password here, the user manager
        # handles that in the database.
        RiverraftingUser.objects.create(name=user.name,
                                        email=user.email,
                                        person_nr=user.person_nr,
                                        password=password,
                                        is_utn_member=True)

        user.status = "confirmed"
        user.save()
        return HttpResponseRedirect('/temp/')

    context = {
        'uid': uid,
        'form': form
    }
    return render(request, 'registrationSystem/create_account.html', context)


def temp(request):
    return render(request, 'registrationSystem/temp.html')
