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

    password_check = CharField(
        widget=PasswordInput(),
        label='Confirm your password'
    )

    phone_nr = PhoneNumberField()

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
            'name': TextInput(),
            'person_nr': TextInput(),
            'email': EmailInput(),
            'password': PasswordInput(),
        }

        field_order = [
            'name', 'person_nr', 'email', 'phone_nr',
            'password', 'password_check'
        ]


class CreateGroupForm(CreateAccountForm):
    def __init__(self, *args, **kwargs):
        super(CreateGroupForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs['readonly'] = 'readonly',
        self.fields["person_nr"].widget.attrs['readonly'] = 'readonly',
        self.fields["email"].widget.attrs['readonly'] = 'readonly'


class JoinGroupForm(CreateAccountForm):
    def __init__(self, *args, group, **kwargs):
        super(CreateAccountForm, self).__init__(*args, **kwargs)
        self.group = group

    def clean(self):
        group_count = get_user_model().objects.filter(
            belongs_to_group=self.group
        ).count()

        if group_count >= RiverRaftingTeam.max_team_members:
            raise ValidationError(
                "The team you are trying to join is already full!",
                code='team_full'
            )


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
            'environment_raft',
            'presentation',
        ]

        labels = {
            'evironment_raft': 'I want an environmentally friendly raft',
            'presentation': 'Group description',
        }

        widgets = {
            'environment_raft': CheckboxInput(
                attrs={'disabled': True}
            ),
            'presentation': TextInput(attrs={'readonly': 'readonly'}),
        }
