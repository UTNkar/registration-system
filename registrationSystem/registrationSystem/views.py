from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import RiverraftingUser
from .forms import CreateAccountForm

def create_account(request, uid):
    form = CreateAccountForm()
    user = get_object_or_404(RiverraftingUser, id=uid)
    context = {
        # 'uid':
        'form': form,
        'name': user.name,
        'person_nr': user.person_nr,
        'email': user.email
    }
    return render(request, 'registrationSystem/create_account.html', context)
