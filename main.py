from flask import Flask, request, render_template
from markupsafe import escape
import random


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
        return {'red_player_state': self.red_state, 'blue_player_state': self.blue_state}


class ConnectionHandler:
    def __init__(self):
        self.first_start_request = True
        self.active_game = None

    def is_first_game_request(self):
        return self.first_start_request

    def wait_for_second_player(self, first_player):
        self.first_start_request = False
        self.active_game = {'first_player': first_player}

    def start_game(self, second_player):
        self.active_game['second_player'] = second_player
        self.active_game['game_state'] = Game(self.active_game['second_player'], self.active_game['second_player'])
        return self.active_game['game_state']


app = Flask(__name__)
app.connection_handler = ConnectionHandler()


@app.route('/')
def index():
    """
    :return: return the front-end index
    """
    return render_template('index.html')


@app.route('/start_game', methods=['GET'])
def start_game():
    if app.connection_handler.is_first_game_request():
        app.connection_handler.wait_for_second_player(request.remote_addr)
        return 'Waiting For Second Player'

    if app.connection_handler.active_game['first_player'] == request.remote_addr:
        return 'The same player entered twice'

    if 'first_player' in app.connection_handler.active_game and \
            'second_player' in app.connection_handler.active_game:
        return 'The game already initialized'

    game = app.connection_handler.start_game(request.remote_addr)
    return game.to_response()
