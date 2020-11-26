from abc import ABC, abstractmethod


class AbstractPayment(ABC):
    """
    Provides methods for handling payments on pay.utn.se
    """
    @abstractmethod
    def get_order_rows_and_cost(self, team_leader):
        """
        Should create order rows for pay.utn.se and return
        the rows and the total cost
        """
        pass
