from django.shortcuts import render, redirect
from registrationSystem.models import InterestCheck
from registrationSystem.forms import InterestCheckForm


async def start(request):
    if request.POST:
        form = InterestCheckForm(request.POST)

        if form.is_valid():
            interest_check_obj = InterestCheck(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                personnr=form.cleaned_data['personnr']
            )

            return render(request,
                          "status_page.html",
                          {'interest_user': interest_check_obj})
    else:
        form = InterestCheckForm()
    return render(request, "start_page.html", {'form': form})
