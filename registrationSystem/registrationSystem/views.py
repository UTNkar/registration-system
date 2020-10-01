from django.shortcuts import render, redirect
from registrationSystem.models import InterestCheck
from registrationSystem.forms import InterestCheckForm

async def start(request):
    if request.method == 'POST':
        form = InterestCheckForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/ticket-system/')
    else:
        form = InterestCheckForm()
    return render(request, "start_page.html", {'form': form})
