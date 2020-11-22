from .abstract_payment_base import AbstractPayment
from registrationSystem.models import RiverRaftingCost
from .order_rows.forska_order_rows import forska_order_rows
from .order_rows.order_row_model import OrderRow


class ForskaPayment(AbstractPayment):
    def get_order_rows_and_cost(self, team_leader):
        team = team_leader.belongs_to_group

        number_of_lifevests = team.get_number_of_lifevests()
        number_of_wetsuits = team.get_number_of_wetsuits()
        number_of_helmets = team.get_number_of_helmets()

        costs = RiverRaftingCost.load()

        # The costs must be in ören, required by pay.utn.se
        lifevest_cost = number_of_lifevests * costs.lifevest * 100
        wetsuit_cost = number_of_wetsuits * costs.wetsuit * 100
        helmet_cost = number_of_helmets * costs.helmet * 100
        raft_fee_cost = costs.raft_fee * 100

        raft_fee = OrderRow(forska_order_rows['raft_fee'])
        raft_fee.set_amount(raft_fee_cost)

        lifevest = OrderRow(forska_order_rows['lifevest'])
        lifevest.set_quantity(number_of_lifevests)
        lifevest.set_amount(lifevest_cost)

        wetsuit = OrderRow(forska_order_rows['wetsuit'])
        wetsuit.set_quantity(number_of_wetsuits)
        wetsuit.set_amount(wetsuit_cost)

        helmet = OrderRow(forska_order_rows['helmet'])
        helmet.set_quantity(number_of_helmets)
        helmet.set_amount(helmet_cost)

        items_to_buy = []

        # If no one in the team wants a certain item,
        # it should not be shown on pay.utn.se
        total_cost = 0
        for row in [raft_fee, lifevest, wetsuit, helmet]:
            if row.get_quantity() > 0:
                items_to_buy.append(row.to_dict())
                print(row.get_amount())
                total_cost += row.get_amount()

        return items_to_buy, total_cost
