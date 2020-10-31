from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.urls import reverse
from registrationSystem.models import InterestCheck
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
    return render(request, "register_page.html", {'form': form})


def status(request):
    interest_check_id = request.session['interest_check_id']
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

