from django.shortcuts import render
from django.http import HttpResponse
from .models import RiverraftingUser

def create_account(request, uid):
    user= RiverraftingUser.objects.get(id=uid)
    context = {
        # 'uid':
        'name': user.name,
        'personnummer': user.person_nr,
        'email': user.email
    }
    return render(request, 'registrationSystem/create_account.html', context)
