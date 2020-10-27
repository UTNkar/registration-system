from django.forms import ModelForm
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
                    'password']
