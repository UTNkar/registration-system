from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import RiverraftingUser

def create_account(request, uid):
    user = get_object_or_404(RiverraftingUser, id=uid)
    context = {
        # 'uid':
        'name': user.name,
        'personnummer': user.person_nr,
        'email': user.email
    }
    return render(request, 'registrationSystem/create_account.html', context)
