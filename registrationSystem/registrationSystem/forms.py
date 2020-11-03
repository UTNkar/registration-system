from django.forms import ModelForm
from django import forms
from registrationSystem.models import InterestCheck
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
