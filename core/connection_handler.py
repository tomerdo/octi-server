from core.game import Game


class ConnectionHandler:
    """
    Handles the logic between the client interaction and the server logic representation
    """

    def __init__(self):
        self.first_start_request = True
        self.active_game = None
        self.last_result = {'status': 'A start request has\'nt been received'}

    def game_started(self):
        """
        :return: predicate that return true iff the game is initialized
        """
        return self.active_game is not None and 'first_player' in self.active_game and 'second_player' in self.active_game

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

    def is_same_connection(self, remote_addr):
        return self.active_game['first_player'] == remote_addr

    def update_last_result(self, result):
        self.last_result = result

    def get_last_result(self):
        return self.last_result
