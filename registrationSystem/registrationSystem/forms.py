from django.forms import ModelForm
from registrationSystem.models import InterestCheck
from registrationSystem.fields import PersonNumberField


class InterestCheckForm(ModelForm):

    personnr = PersonNumberField()

    class Meta:
        model = InterestCheck
        fields = ['name',
                  'email',
                  'personnr']
