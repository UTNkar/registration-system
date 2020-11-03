from django import forms
from django.forms import (
    ModelForm, CharField, TextInput, EmailInput, PasswordInput, ValidationError
)
from registrationSystem.models import InterestCheck, RiverraftingUser
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
        model = RiverraftingUser
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
