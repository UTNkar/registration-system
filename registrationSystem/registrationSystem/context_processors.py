from .models import RiverRaftingRaffleState

def river_rafting_raffle_state(request):
    return {'river_rafting_raffle_state': RiverRaftingRaffleState.load()}
