from django.shortcuts import render, redirect
from django.urls import reverse
from registrationSystem.models import InterestCheck
from registrationSystem.forms import InterestCheckForm


def start(request):
    if request.POST:
        form = InterestCheckForm(request.POST)

        if form.is_valid():
            interest_check_obj, _ = InterestCheck.objects.get_or_create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                personnr=form.cleaned_data['personnr'],
            )
            request.session['interest_check_id'] = interest_check_obj.id
            return redirect(reverse('status'))
    else:
        form = InterestCheckForm()
    return render(request, "start_page.html", {'form': form})


def status(request):
    interest_check_id = request.session['interest_check_id']
    interest_check_obj = InterestCheck.objects.get(id=interest_check_id)

    if interest_check_obj.status == "mail unconfirmed":
        template = "mail_unconfirmed.html"
    elif interest_check_obj.status == "mail confirmed":
        template = "mail_confirmed.html"
    elif interest_check_obj.status == "won":
        template = "won.html"
    elif interest_check_obj.status == "lost":
        template = "lost.html"
    elif interest_check_obj.status == "reapplying":
        template = "reapplying.html"
    elif interest_check_obj.status == "pending":
        template = "pending.html"
    elif interest_check_obj.status == "declined":
        template = "declined.html"

    return render(request,
                  "status/" + template,
                  {"interest_check_obj": interest_check_obj})
