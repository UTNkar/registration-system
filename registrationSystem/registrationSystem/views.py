from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from registrationSystem.models import InterestCheck, Group, User, RiverraftingUser, get_group_model
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
    return render(request, "start_page.html", {'form': form })


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
    group = Group.objects.get(id=user.belongs_to_group.id)
    others = user_model.objects.filter(belongs_to_group=group.id).exclude(id=user_id)

    return render(request,
                  "overview.html",
                  { "user": user,
                    "group": group,
                    "others": others, })
