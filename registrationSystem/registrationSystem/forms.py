from django.forms import ModelForm, TextInput, EmailInput
from registrationSystem.models import InterestCheck, RiverraftingUser


class InterestCheckForm(ModelForm):
    class Meta:
        model = InterestCheck
        fields = ['name',
                  'email',
                  'person_nr']


class CreateAccountForm(ModelForm):
    class Meta:
        model = RiverraftingUser
        fields = [  'name',
                    'person_nr',
                    'email',
                    'password' ]

        labels = {  'name': 'Namn',
                    'person_nr': 'Personnummer',
                    'email': 'E-postadress' }

        widgets = { 'name': TextInput(attrs={'disabled': True}),
                    'person_nr': TextInput(attrs={'disabled': True}),
                    'email': EmailInput(attrs={'disabled': True}) }
