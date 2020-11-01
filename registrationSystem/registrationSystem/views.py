from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import InterestCheck, RiverraftingUser
from .forms import CreateAccountForm

def create_account(request, uid):
    user = get_object_or_404(InterestCheck, id=uid)
    form = CreateAccountForm(request.POST or None)
    # initial={  'name': user.name,
    #                                                     'person_nr': user.person_nr,
    #                                                     'email': user.email }   )

    if form.is_valid():
        # Linus jobbar på en lösning för att automatiskt hasha alla lösenord i databasen.
        # Den här funktionen behöver i nuläget inte hasha själv!
        data = form.cleaned_data
        del data['password_check'] # Creating the user from data gives error if included since it matches no field in the model.
        RiverraftingUser.objects.create(**data, is_utn_member=True)
        return HttpResponseRedirect('/temp/')

    context = {
        'uid': uid,
        'form': form
    }
    return render(request, 'registrationSystem/create_account.html', context)



def temp(request):
    return render(request, 'registrationSystem/temp.html')
