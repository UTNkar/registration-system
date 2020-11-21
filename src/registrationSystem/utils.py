from django.core import validators
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import requests
from registrationSystem.models import EmailConfirmation


def send_win_email(user):
    """
    Call this function when a user wins a raft (i.e. the status of
    the RaffleEntry turns 'won')
    to send an email containing a unique link to create a full account.

    Parameters:
    user: RaffleEntry of the person who won.

    Returns:
    nothing
    """
    # The connector binds the randomized token
    # to the RaffleEntry from which the account
    # information will be retreived.
    connector = EmailConfirmation.objects.create(raffleEntryId=user)
    connector.save()

    message = render_to_string(
        'email/create-account_email.html',
        {
            'name': user.name,
            'domain': 'localhost:8000',
            'token': connector.id,
        }
    )
    to_email = user.email
    email = EmailMessage(
        'You have won a raft!',
        message,
        to=[to_email]
    )
    email.send()

    return


def is_utn_member(person_nr):
    """
    Call this function to see if a person is a member of the
    student union UTN.

    Params:
    person_nr: The social security number of the person, as a string

    Returns:
    True if the person is a member, else False.
    """

    r = requests.post(
        'https://utn.se/member_check_api/',
        {'ssn': person_nr}
    )

    return r.json()['is_member']


# TODO: Change regex to only support YYYYMMDD-XXXX
class SSNValidator(validators.RegexValidator):
    century = r'[1-2][0|9]'  # YY-- Only allows 19-- and 20--
    decade = r'[0-9]{2}'  # --YY
    month = r'[0-1][0-9]'
    day = r'[0-3][0-9]'
    last_four = r'(T|t|[0-9])[0-9]{3}'  # Allows T-number SSN

    def __init__(self):
        regex_pattern = \
            r'^(' + self.century + r')?' + \
            self.decade + \
            self.month + \
            self.day + \
            r'(-|\+)?' + \
            self.last_four + \
            r'$'

        super(SSNValidator, self).__init__(
            regex=regex_pattern,
            message='Use the format YYYYMMDD-XXXX.'
        )
