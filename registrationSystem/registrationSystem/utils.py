from django.core import validators
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.exceptions import FieldError
import requests
from registrationSystem.models import EmailConfirmations


def user_has_won(user):
    """
    Call this function when a user wins a raft.
    The function sets the status of the InterestCheck to 'won'
    and calls the function send_win_email() to send an email
    containing a unique link to create a full account.

    Parameters:
    user: InterestCheck of the person who won.

    Returns:
    nothing
    """
    user.status = 'won'
    user.save()
    send_email(user)
    return


def send_email(user):
    """
    Call this function to send an email containing a unique link with the
    user's InterestCheck.
    Used to confirm registration email or to create a full account.

    Parameters:
    user: InterestCheck of the person to send the email.

    Returns:
    nothing
    """

    # The connector binds the randomized token to the InterestCheck
    # from which the account information will be retreived.
    connector = EmailConfirmations.objects.create(interestCheckId=user)
    connector.save()

    status = user.status
    if status == 'mail unconfirmed':
        emailtitle = 'Activate your account'
        template = 'email/confirm_email.html'
    elif status == 'won':
        emailtitle = 'You have won a raft!'
        template = 'email/create-account_email.html'
    else:
        raise FieldError('Incorrect user status in order to send an email!')

    # TODO: Set domain to the actual domain on production.
    message = render_to_string(
                template,
                {
                    'name': user.name,
                    'domain': 'localhost:8000',
                    'token': connector.id,
                }
            )
    to_email = user.email
    email = EmailMessage(
        emailtitle,
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
