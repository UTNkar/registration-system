from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import InterestCheck, RiverraftingUser
from .forms import CreateAccountForm

def create_account(request, uid):
    user = get_object_or_404(InterestCheck, id=uid)
                                    'email': user.email })
    context = {
        'uid': uid,
        'form': form
    }
    return render(request, 'registrationSystem/create_account.html', context)



def received(request, uid):
    print(request.POST)
    received_form = CreateAccountForm(request.POST)
    if received_form.is_valid():
        # Linus jobbar på en lösning för att automatiskt hasha alla lösenord i databasen.
        # Den här funktionen behöver i nuläget inte hasha själv!
        data = received_form.cleaned_data
        del data['password_check']
        RiverraftingUser.objects.create(**data, is_utn_member=True)
        return HttpResponseRedirect('/temp/')

    context = {
        'form': received_form,
        'uid': uid
    }
    return render(request, 'registrationSystem/create_account.html', context)


def temp(request):
    return render(request, 'registrationSystem/temp.html')
