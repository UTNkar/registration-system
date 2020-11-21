import requests
from phpserialize import dumps
from django.contrib.auth import get_user_model
from django.conf import settings
from registrationSystem.models import RiverraftingCost


def getItemsToBuy(team_leader):
    number_of_lifevests = 0
    number_of_wetsuits = 0
    number_of_helmets = 0

    team_members = get_user_model().objects.filter(
        belongs_to_group=team_leader.belongs_to_group
    )

    costs = RiverraftingCost.load()

    for user in team_members:
        if user.lifevest_size:
            number_of_lifevests += 1
        if user.wetsuite_size:
            number_of_wetsuits += 1
        if user.helmet_size:
            number_of_helmets += 1

    # The costs must be in ören, required by pay.utn.se
    lifevest_cost = number_of_lifevests * costs.lifevest * 100
    wetsuit_cost = number_of_wetsuits * costs.wetsuit * 100
    helmet_cost = number_of_helmets * costs.helmet * 100

    lifevest_row = {
        'name': "Life vests",
        'description': "Make you float. floaet = good!",
        'category': 'participation_fee',
        'quantity': number_of_lifevests,
        'unit': 'st',
        'amount': lifevest_cost,
        'vat': 0
    }

    wetsuit_row = {
        'name': "Wetsuit",
        'description': "Wetsuit to survive water when cold",
        'category': 'participation_fee',
        'quantity': number_of_wetsuits,
        'unit': 'st',
        'amount': wetsuit_cost,
        'vat': 0
    }

    helmet_row = {
        'name': "Helmet",
        'description': "Protect head! Head dmg -1",
        'category': 'participation_fee',
        'quantity': number_of_lifevests,
        'unit': 'st',
        'amount': helmet_cost,
        'vat': 0
    }
    items_to_buy = []

    # If no one in the team wants a certain item,
    # it should not be shown on pay.utn.se
    if number_of_helmets > 0:
        items_to_buy.append(helmet_row)

    if number_of_wetsuits > 0:
        items_to_buy.append(wetsuit_row)

    if number_of_lifevests > 0:
        items_to_buy.append(lifevest_row)

    items_to_buy = [
        lifevest_row,
        wetsuit_row,
        helmet_row
    ]

    total_items_cost = lifevest_cost + wetsuit_cost + helmet_cost
    return items_to_buy, total_items_cost


# Kommer krävas massa dokumentation!
# Försöker djangofiera ett kall på det gamla pay Api:et som finns.
# Vad är det som händer här? Vad är det för olika items och vart får man tag på
# alla olika nycklar? Api keys och diverse Id
# 'catogory' Ugly old solution sets it to 'participation_fee' all the time.
def createPaymentLink(user):
    rows, total_cost = getItemsToBuy(user)

    raft_fee = {
        'name': "Raft fee",
        'description': "The base fee for a raft in the River Rafting",
        'category': 'participation_fee',
        'quantity': 1,
        'unit': 'st',
        'amount': 10000,  # Must be in ören
        'vat': 0
    }

    order_rows = [raft_fee] + rows
    total_cost += raft_fee['amount']

    # Pay.utn.se wants first and last name.
    # Registration page asks for name in one field and thats why we split
    # Might be derpy with some names? TODO Test cases if needed
    userNameSplitted = user.name.split(' ')
    first_name = userNameSplitted.pop(0)
    last_name = userNameSplitted

    items = {
        # 'id' is the reference that will be shown in pay.utn.se
        'id': user.belongs_to_group.name + ' ' + user.name,
        # 'receiver_id is the id number for the account on pay.utn.se
        #  that will receive the money.
        'receiver_id': settings.PAY_RECEIVER_ID,
        # 'callback_url is required by pay.utn.se but it doesn't use it lol
        'callback_url': 'https://nowhere',
        'national_identification_number': user.person_nr,
        'first_name': first_name,
        'last_name': last_name,
        'email': user.email,
        # 'title' and 'description' seems to not be used in pay.utn.se
        'title': 'not used',
        'description': 'not used',
        'language': 'en',
        'payment_method': 'card',
        'order_rows': dumps(order_rows),
        'total_amount': total_cost
    }

    r = requests.post('https://pay.utn.se/api/new_payment', data=items)

    if r.status_code != 200:
        print(r.text)
        raise ValueError("Recevied invalid response from pay.utn.se")

    return 'https://pay.utn.se/payments/confirm/' + r.text.strip()
