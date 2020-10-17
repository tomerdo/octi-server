from core.game import Game


class ConnectionHandler:
    """
    Handles the logic between the client interaction and the server logic representation
    """
    def __init__(self):
        self.first_start_request = True
        self.active_game = None

    def game_start(self):
        return self.active_game is None or 'second_player' not in self.active_game

    def is_first_game_request(self):
        return self.first_start_request

    def wait_for_second_player(self, first_player):
        self.first_start_request = False
        self.active_game = {'first_player': first_player}

    def start_game(self, second_player):
        self.active_game['second_player'] = second_player
        self.active_game['game_state'] = Game(self.active_game['second_player'], self.active_game['second_player'])
        return self.active_game['game_state']

    def game_repr(self):
        return self.active_game['game_state'].to_response()
