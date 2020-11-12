from django import forms
from django.forms import (
    ModelForm, CharField, TextInput, EmailInput, PasswordInput, ValidationError, CheckboxInput
)
from registrationSystem.models import InterestCheck, RiverraftingProfile, RiverraftingGroup
from registrationSystem.fields import PersonNumberField

class InterestCheckForm(ModelForm):
    person_nr = PersonNumberField()

    status = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = InterestCheck
        fields = ['name',
                  'email',
                  'person_nr',
                  'status']

class CreateAccountForm(ModelForm):

    def clean_password_check(self):
        password = self.cleaned_data.get('password')
        password_check = self.cleaned_data.get('password_check')

        if not password_check:
            raise ValidationError("You must confirm you password!")
        if password != password_check:
            raise ValidationError("The passwords do not match!")
        return password_check

    password_check = CharField(
        widget=PasswordInput(),
        label='Confirm your password'
    )

    class Meta:
        model = RiverraftingProfile
        fields = [
            'name',
            'person_nr',
            'email',
            'password'
        ]

        labels = {
            'name': 'Full name',
            'person_nr': 'Social security number',
            'email': 'E-mail address',
            'password': 'Choose a password'
        }

        widgets = {
            'name': TextInput(attrs={'readonly': 'readonly'}),
            'person_nr': TextInput(attrs={'readonly': 'readonly'}),
            'email': EmailInput(attrs={'readonly': 'readonly'}),
            'password': PasswordInput(),
        }

# todo: change to single user and instead have relational models depending on user type
class RiverraftingProfileForm(ModelForm):

    class Meta:
        model = RiverraftingProfile

        fields = [
            'name',
            'email',
        ]

        labels = {
            'name': 'Full name',
            'email': 'E-mail address',
        }

        widgets = {
            'name': TextInput(attrs={'readonly': 'readonly'}),
            'email': EmailInput(attrs={'readonly': 'readonly'}),
        }


# todo: change to single user and instead have relational models depending on user type
class RiverraftingGroupForm(ModelForm):

    class Meta:
        model = RiverraftingGroup

        fields = [
            'number',
            'environment_raft',
            'presentation',
        ]

        labels = {
            'number': 'Start number',
            'evironment_raft': 'I want an environmentally friendly raft',
            'presentation': 'Group description',
        }

        widgets = {
            'number': TextInput(attrs={'readonly': 'readonly', 'disabled': 'disabled'}),
            'environment_raft': CheckboxInput(attrs={'onclick': 'return false'}),
            'presentation': TextInput(attrs={'readonly': 'readonly'}),
        }
