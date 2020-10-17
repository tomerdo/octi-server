import random


class Game:
    def __init__(self, first_player, second_player):
        red_player, blue_player = choose_red_and_blue_randomly(first_player, second_player)
        self.red_player = red_player
        self.blue_player = blue_player
        self.round_num = 0
        self.action_num = 0
        self.blue_state = create_state(blue_player)
        self.red_state = create_state(red_player)

    def to_response(self):
        return {'status': 'active', 'red_player_state': self.red_state, 'blue_player_state': self.blue_state, \
                'round_num': self.round_num, 'action_num': self.action_num}


def choose_red_and_blue_randomly(first_player, second_player):
    """
    This is an helper function - to randomly chose red and blue players
    :param first_player: first_player address
    :param second_player: second_player address
    :return:
    """
    players = [first_player, second_player]
    red_player = random.choice(players)
    players.remove(red_player)
    blue_player = players.pop()
    return red_player, blue_player


def create_state(player):
    return []
