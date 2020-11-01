from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from registrationSystem.models import InterestCheck, Group, User, RiverraftingUser
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
    user_model = get_user_model()
    user = user_model.objects.get(id=2)

    group = Group.objects.get(leader=user.id)
    others = user_model.objects.filter(belongs_to_group=group.id)
    editing = [false for x in others]

    return render(request,
                  "overview.html",
                  { "user": user,
                    "group": group,
                    "others": others,
                    })
