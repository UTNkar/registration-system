class OrderRow():
    def __init__(self, fields):
        self.name = fields['name']
        self.description = fields['description']
        self.unit = fields['unit']
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
