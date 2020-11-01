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

    if form.is_valid():
        password = form.cleaned_data['password']
        # There is no need to encrypt the password here, the user manager handles that in the database.
        RiverraftingUser.objects.create(name=user.name,
                                        email=user.email,
                                        person_nr=user.person_nr,
                                        password=password,
                                        is_utn_member=True)

        user.status = "confirmed"
        user.save()
        return HttpResponseRedirect('/temp/')

    context = {
        'uid': uid,
        'form': form
    }
    return render(request, 'registrationSystem/create_account.html', context)



def temp(request):
    return render(request, 'registrationSystem/temp.html')
