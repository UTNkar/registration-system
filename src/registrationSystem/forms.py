from django import forms
from django.forms import (
    ModelForm, CharField, TextInput, EmailInput,
    PasswordInput, ValidationError, CheckboxInput,
    Select
)
from registrationSystem.models import (
    RaffleEntry, RiverRaftingUser, RiverRaftingTeam
)
from registrationSystem.fields import PersonNumberField, PhoneNumberField
from django.contrib.auth import get_user_model


class RaffleEntryForm(ModelForm):
    person_nr = PersonNumberField()

    status = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = RaffleEntry
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

    phone_nr = PhoneNumberField()
    password_check = CharField(
        widget=PasswordInput(),
        label='Confirm your password'
    )

    class Meta:
        model = get_user_model()
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

        field_order = [
            'name', 'person_nr', 'email', 'phone_nr',
            'password', 'password_check'
        ]


class RiverRaftingUserForm(ModelForm):
    class Meta:
        model = RiverRaftingUser

        fields = [
            'name',
            'email',
            'lifevest_size'
        ]

        labels = {
            'name': 'Full name',
            'email': 'E-mail address',
            'lifevest_size': 'Lifevest Size',
        }

        widgets = {
            'name': TextInput(attrs={'readonly': 'readonly'}),
            'email': EmailInput(attrs={'readonly': 'readonly'}),
            'lifevest_size': Select(attrs={'disabled': True})
        }


class RiverRaftingTeamForm(ModelForm):
    class Meta:
        model = RiverRaftingTeam

        fields = [
            'name',
            'environment_raft',
            'presentation',
        ]

        labels = {
            'name': 'Team name',
            'evironment_raft': 'I want an environmentally friendly raft',
            'presentation': 'Group description',
        }

        widgets = {
            'name': TextInput(attrs={'readonly': 'readonly'}),
            'environment_raft': CheckboxInput(
                attrs={'disabled': True}
            ),
            'presentation': TextInput(attrs={'readonly': 'readonly'}),
        }

