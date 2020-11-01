from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import InterestCheck, RiverraftingUser
from .forms import CreateAccountForm

def create_account(request, uid):
    user = get_object_or_404(InterestCheck, id=uid)

    if request.method == "POST":
        form = CreateAccountForm(request.POST)
    else:
        form = CreateAccountForm(initial={ 'name': user.name, 'person_nr': user.person_nr, 'email': user.email })
        # Doing it this way avoids triggering validation errors since the password fields are not
        # initially filled.
        # Initializing form = CreateAccountForm(request.POST or initial={...}) triggers the errors.

    if form.is_valid():
        # Linus jobbar på en lösning för att automatiskt hasha alla lösenord i databasen.
        # Den här funktionen behöver i nuläget inte hasha själv!
        password = form.cleaned_data['password']
        RiverraftingUser.objects.create(name=user.name,
                                        email=user.email,
                                        person_nr=user.person_nr,
                                        password=password,
                                        is_utn_member=True)
        return HttpResponseRedirect('/temp/')

    context = {
        'uid': uid,
        'form': form
    }
    return render(request, 'registrationSystem/create_account.html', context)



def temp(request):
    return render(request, 'registrationSystem/temp.html')
