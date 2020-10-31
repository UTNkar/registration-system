from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import InterestCheck, RiverraftingUser
from .forms import CreateAccountForm

def create_account(request, uid):
    user = get_object_or_404(InterestCheck, id=uid)
                                    'email': user.email })
    context = {
        # 'uid':
        'form': form,
        # 'name': user.name,
        # 'person_nr': user.person_nr,
        # 'email': user.email
    }
    return render(request, 'registrationSystem/create_account.html', context)

def received(request):
    print(request.POST)
    received_form = CreateAccountForm(request.POST)
    if received_form.is_valid():
        data = received_form.cleaned_data
        del data['password_check']
        RiverraftingUser.objects.create(**data, is_utn_member=True)
    else:
        print('NOT VALID')

    context = {
        'name': request.POST.get('name'),
        'email': request.POST.get('email'),
        'person_nr': request.POST.get('person_nr')
    }
    return render(request, 'registrationSystem/temp.html', context)
