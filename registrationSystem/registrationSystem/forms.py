from django.forms import ModelForm, CharField, TextInput, EmailInput, PasswordInput, ValidationError
from registrationSystem.models import InterestCheck, RiverraftingUser


class InterestCheckForm(ModelForm):
    class Meta:
        model = InterestCheck
        fields = ['name',
                  'email',
                  'person_nr']


class CreateAccountForm(ModelForm):

    def clean_password_check(self):
        password = self.cleaned_data.get('password')
        password_check = self.cleaned_data.get('password_check')

        if not password_check:
            raise ValidationError("Du måste bekräfta ditt lösenord!")
        if password != password_check:
            raise ValidationError("Lösenorden matchar inte!")
        return password_check


    password_check = CharField( widget=PasswordInput(),
                                label='Bekräfta ditt lösenord'  )
    class Meta:
        model = RiverraftingUser
        fields = [  'name',
                    'person_nr',
                    'email',
                    'password' ]

        labels = {  'name': 'Namn',
                    'person_nr': 'Personnummer',
                    'email': 'E-postadress',
                    'password': 'Välj ett lösenord' }

        widgets = { 'name': TextInput(attrs={'disabled': True}),
                    'person_nr': TextInput(attrs={'disabled': True}),
                    'password': PasswordInput(), }
