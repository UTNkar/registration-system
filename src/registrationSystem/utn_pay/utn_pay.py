import requests
from phpserialize import dumps
from django.conf import settings
from .payment_classes.forska_payment import ForskaPayment


def get_order_rows_model():
    """
    Returns the payment model for the event set in settings
    """
    if settings.EVENT == 'RIVERRAFTING':
        return ForskaPayment()


def get_payment_link(team_leader):
    """
    Creates a payment on pay.utn.se and returns the link to where
    a user will make the payment

    Params:

    team_leader: A user that is also the team leader.

    Returns:

    A link to pay.utn.se where the user should go to make their payment

    Raises:

    ValueError if team_leader is not a team leader or if pay
    gives an invalid response
    """
    if not team_leader.is_team_leader():
        raise ValueError("User is not a team leader")

    order_rows_model = get_order_rows_model()
    rows, total_cost = order_rows_model.get_order_rows_and_cost(team_leader)

    # Pay.utn.se wants first and last name while we store the first and last
    # name as a whole. Therefor we split the name to fake a last name
    userNameSplitted = team_leader.name.split(' ')
    first_name = userNameSplitted.pop(0)
    last_name = " ".join(userNameSplitted)

    items = {
        # 'id' is the reference that will be shown in pay.utn.se
        'id': team_leader.belongs_to_group.name + ', ' + team_leader.name,
        # 'receiver_id is the id number for the account on pay.utn.se
        #  that will receive the money.
        'receiver_id': settings.PAY_RECEIVER_ID,
        # 'callback_url is required by pay.utn.se but it doesn't use it lol
        'callback_url': 'https://nowhere',
        'national_identification_number': team_leader.person_nr,
        'first_name': first_name,
        'last_name': last_name,
        'email': team_leader.email,
        # 'title' and 'description' seems to not be used in pay.utn.se
        'title': 'not used',
        'description': 'not used',
        'language': 'en',
        'payment_method': 'card',
        'order_rows': dumps(rows),
        'total_amount': total_cost
    }

    r = requests.post('https://pay.utn.se/api/new_payment', data=items)

    if r.status_code != 200:
        print(r.text)
        raise ValueError("Recevied invalid response from pay.utn.se")

    return 'https://pay.utn.se/payments/confirm/' + r.text.strip()
