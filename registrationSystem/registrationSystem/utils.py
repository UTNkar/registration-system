from django.core import validators
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from registrationSystem.models import EmailConfirmations


def send_win_email(user):
    """
    Call this function when a user wins a raft (i.e. the status of
    the InterestCheck turns 'won')
    to send an email containing a unique link to create a full account.

    Parameters:
    user: InterestCheck of the person who won.

    Returns:
    nothing
    """

    # The connector binds the randomized token
    # to the InterestCheck from which the account
    # information will be retreived.
    connector = EmailConfirmations.objects.create(interestCheckId=user)
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
