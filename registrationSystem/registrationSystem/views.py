from django.shortcuts import render
from django.http import HttpResponse

def create_account(request):
    context = {
        'uid': '123a'
    }
    return render(request, 'registrationSystem/create_account.html', context)
