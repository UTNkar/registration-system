import requests
from phpserialize import dumps
from django.conf import settings
from registrationSystem.models import RiverraftingCost
from .forska_fields import forska_fields
from abc import ABC, abstractmethod


class OrderRow():
    def __init__(self, fields):
        self.name = fields['name']
        self.description = fields['description']
        self.unit = fields['unit']
        if 'amount' in fields:
            self.amount = fields['amount']
        if 'quantity' in fields:
            self.quantity = fields['quantity']

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_amount(self, amount):
        self.amount = amount

    def get_amount(self):
        if not hasattr(self, 'amount'):
            raise AttributeError(
                "Could not get amount because it has not been set"
            )
        return self.amount

    def get_quantity(self):
        if not hasattr(self, 'quantity'):
            raise AttributeError(
                "Could not get quantity because it has not been set"
            )
        return self.quantity

    def to_dict(self):
        if not hasattr(self, 'quantity'):
            raise AttributeError("Quantity has not been set")
        if not hasattr(self, 'amount'):
            raise AttributeError("Amount has not been set")

        return {
            'name': self.name,
            'description': self.description,
            # 'category' Ugly old solution sets it to 'participation_fee'
            'category': 'participation_fee',
            'quantity': self.quantity,
            'unit': self.unit,
            'amount': self.amount,
            'vat': 0
        }

    def __str__(self):
        return str(self.__dict__)


class AbstractPayment(ABC):
    @abstractmethod
    def get_items_and_cost(self, team_leader):
        pass


class ForskaPayment(AbstractPayment):
    def __init__(self):
        super().__init__()

    def get_items_and_cost(self, team_leader):
        team = team_leader.belongs_to_group

        number_of_lifevests = team.get_number_of_lifevests()
        number_of_wetsuits = team.get_number_of_wetsuits()
        number_of_helmets = team.get_number_of_helmets()

        costs = RiverraftingCost.load()

        # The costs must be in ören, required by pay.utn.se
        lifevest_cost = number_of_lifevests * costs.lifevest * 100
        wetsuit_cost = number_of_wetsuits * costs.wetsuit * 100
        helmet_cost = number_of_helmets * costs.helmet * 100

        raft_fee = OrderRow(forska_fields['raft_fee'])

        lifevest = OrderRow(forska_fields['lifevest'])
        lifevest.set_quantity(number_of_lifevests)
        lifevest.set_amount(lifevest_cost)

        wetsuit = OrderRow(forska_fields['wetsuit'])
        wetsuit.set_quantity(number_of_wetsuits)
        wetsuit.set_amount(wetsuit_cost)

        helmet = OrderRow(forska_fields['helmet'])
        helmet.set_quantity(number_of_helmets)
        helmet.set_amount(helmet_cost)

        items_to_buy = []

        # If no one in the team wants a certain item,
        # it should not be shown on pay.utn.se
        total_cost = 0
        for row in [raft_fee, lifevest, wetsuit, helmet]:
            if row.get_quantity() > 0:
                items_to_buy.append(row.to_dict())
                total_cost += row.get_amount()

        return items_to_buy, total_cost


class RallyPayment(AbstractPayment):
    def get_items_and_cost(self, team_leader):
        raise NotImplementedError()


def get_order_rows_model():
    if settings.EVENT == 'RIVERRAFTING':
        return ForskaPayment()


# Kommer krävas massa dokumentation!
# Försöker djangofiera ett kall på det gamla pay Api:et som finns.
# Vad är det som händer här? Vad är det för olika items och vart får man tag på
# alla olika nycklar? Api keys och diverse Id
def createPaymentLink(team_leader):
    rows, total_cost = get_order_rows_model().get_items_and_cost(team_leader)

    # Pay.utn.se wants first and last name.
    # Registration page asks for name in one field and thats why we split
    # Might be derpy with some names? TODO Test cases if needed
    userNameSplitted = team_leader.name.split(' ')
    first_name = userNameSplitted.pop(0)
    last_name = userNameSplitted

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
