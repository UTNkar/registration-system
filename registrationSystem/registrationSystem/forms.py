from django.forms import ModelForm
from registrationSystem.models import InterestCheck


class InterestCheckForm(ModelForm):
    class Meta:
        model = InterestCheck
        fields = ['name',
                  'email',
                  'personnr']
