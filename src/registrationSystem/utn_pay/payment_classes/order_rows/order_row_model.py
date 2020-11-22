class OrderRow():
    """
    Represents an order row in pay.utn.se. Some fields can be added directly
    when creating the class while others must be added manualy.
    """
    def __init__(self, fields):
        """
        fields must include the following fields:
        name: string - The name of the thing you're paying for
        description: string - Describes what the thing you're paying for is
        unit: string - the unit the describes the amount eg 'st'

        fields can optionally include
        quantity: int - The number of items to buy of the thing you're paying
        for
        """
        self.name = fields['name']
        self.description = fields['description']
        self.unit = fields['unit']
        if 'quantity' in fields:
            self.quantity = fields['quantity']

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_amount(self, amount):
        """
        Sets the amount of money it costs to purchase the thing you're paying
        for. This should be the total cost for for all the items your buying
        of this type.

        e.g. if an item costs 50kr and you buy 3, the amount should be set to
        150 kr
        """
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
            # 'category' Ugly old solution by pay.utn.se sets
            # it to 'participation_fee' for all fields
            'category': 'participation_fee',
            'quantity': self.quantity,
            'unit': self.unit,
            'amount': self.amount,
            # Is required by pay but is rarely used
            'vat': 0
        }

    def __str__(self):
        return str(self.__dict__)
