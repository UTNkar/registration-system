from django.forms import ModelForm
from django import forms
from registrationSystem.models import InterestCheck
from registrationSystem.fields import PersonNumberField


class InterestCheckForm(ModelForm):

    personnr = PersonNumberField()

    status = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = InterestCheck
        fields = ['name',
                  'email',
                  'personnr',
                  'status']
