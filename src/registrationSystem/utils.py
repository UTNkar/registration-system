from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.exceptions import FieldError
import requests
from registrationSystem.models import EmailConfirmation
from django.urls import reverse
from django.shortcuts import redirect


def user_has_won(user, domain):
    """
    Call this function when a user wins a raft.  The function sets the
    status of the raffle entry to 'won' and calls the function
    send_win_email() containing a unique link to create a full
    account.

    Parameters:
    user: RaffleEntry of the person who won.

    domain: The domain the request was made to (request.domain)

    Returns:
    nothing

    """
    user.status = 'won'
    user.save()
    send_email(user, domain)
    return


def send_email(user, domain):
    """
    Call this function to send an email containing a unique link with the
    user's raffle entry.
    Used to confirm registration email or to create a full account.

    Parameters:
    user: RaffleEntry of the person to send the email.

    domain: The domain the request was made to (request.domain)

    Returns:
    nothing
    """

    # The connector binds the randomized token to the RaffleEntry
    # from which the account information will be retreived.
    connector = EmailConfirmation.objects.get_or_create(raffleEntryId=user)
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

    message = render_to_string(
                template,
                {
                    'name': user.name,
                    'domain': domain,
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


def redirect_to_status(request, raffle_entry_id):
    request.session['raffle_entry_id'] = raffle_entry_id
    return redirect(reverse('status'))
