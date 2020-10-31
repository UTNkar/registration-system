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
