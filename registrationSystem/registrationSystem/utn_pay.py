import requests
from phpserialize import dumps
from django.contrib.auth import get_user_model
from django.conf import settings
from registrationSystem.models import RiverraftingUser
from django.contrib.auth.models import User


def getItemsToBuy():

    return

# Kommer krävas massa dokumentation!
# Försöker djangofiera ett kall på det gamla pay Api:et som finns.
# Vad är det som händer här? Vad är det för olika items och vart får man tag på
# alla olika nycklar? Api keys och diverse Id
def createPaymentLink(user_id):

    # user_model = get_user_model()
    user = User.objects.get(pk=user_id)

    order_rows = [
        {
            'name': "Raft fee",
            'description': "The base fee for a raft in the River Rafting",
            'category': 'participation_fee',
            'quantity': 1,
            'unit': 'st',
            'amount': 10000,  # Must be in ören
            'vat': 0
        }
    ]

    items = {
        'id': 42,  # Should be team ID. Will show in pay utn admin page
        'receiver_id': settings.PAY_RECEIVER_ID,
        'callback_url': 'https://nowhere',
        # 'national_identification_number': user.person_nr,
        'national_identification_number': 'Some personnr',
        'first_name': 'Förnamn',
        'last_name': 'efternamn',  # Kolla hur vi ville lösa detta. Ta bort i pay?
        # 'email': user.email,
        'email': 'derp@schnerp.com',
        'title': 'dk testar',
        'description': 'Beskrivning på betalning?',
        'language': 'en',
        'payment_method': 'card',
        'order_rows': dumps(order_rows),
        'total_amount': 10000
    }

    r = requests.post('https://pay.utn.se/api/new_payment', data=items)

    return 'https://pay.utn.se/payments/confirm/' + r.text.strip()
