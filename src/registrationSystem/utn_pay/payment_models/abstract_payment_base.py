from abc import ABC, abstractmethod


class AbstractPayment(ABC):
    @abstractmethod
    def get_order_rows_and_cost(self, team_leader):
        pass
