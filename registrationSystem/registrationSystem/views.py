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
                personnr=form.cleaned_data['personnr']
            )

            request.session['interest_check_id'] = interest_check_obj.id
            return redirect(reverse('status'))
    else:
        form = InterestCheckForm()
    return render(request, "start_page.html", {'form': form})


def status(request):
    return render(request, "status_page.html")
