from django.shortcuts import render, redirect
from django.urls import reverse
from registrationSystem.models import InterestCheck, Group, User
from registrationSystem.forms import InterestCheckForm

def start(request):
    if request.POST:
        form = InterestCheckForm(request.POST)

        if form.is_valid():
            interest_check_obj, _ = InterestCheck.objects.get_or_create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                personnr=form.cleaned_data['personnr'],
                status=form.cleaned_data['status']
            )
            status = form.cleaned_data['status']
            if not status:
                print('pls')

            print('heloa2')
            print(status)
            request.session['interest_check_id'] = interest_check_obj.id
            return redirect(reverse('status'))
    else:
        form = InterestCheckForm(initial={'status': 'Mail-Unconfirmed'})
        print('heloa')
        print(form['status'])
    return render(request, "start_page.html", {'form': form})


def status(request):
    interest_check_id = request.session['interest_check_id']
    interest_check_obj = InterestCheck.objects.get(id=interest_check_id)
    return render(request,
                  "status_page.html",
                  {"interest_check_obj": interest_check_obj})

def overview(request):
    fields = User._meta.get_fields()
    return render(request,
                  "overview.html",
                  {"fields": fields})
