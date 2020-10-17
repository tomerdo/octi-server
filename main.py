from flask import Flask, request, render_template
from core.connection_handler import ConnectionHandler

app = Flask(__name__)
app.connection_handler = ConnectionHandler()


@app.route('/')
def index():
    """
    :return: return the front-end index
    """
    return render_template('index.html')


@app.route('/game_state')
def get_game_state():
    if not app.connection_handler.game_started():
        return {'status': 'Not initialized'}
    return app.connection_handler.game_repr()


@app.route('/start_game', methods=['GET'])
def start_game():
    """
    :return: representation of a new game if two player are connected,
    other message describing the state otherwise.
    """
    if app.connection_handler.is_first_game_request():
        app.connection_handler.wait_for_second_player(request.remote_addr)
        return {'status': 'Waiting For Second Player'}

    if app.connection_handler.active_game['first_player'] == request.remote_addr:
        return {'status': 'The same player entered twice'}

    if 'first_player' in app.connection_handler.active_game and \
            'second_player' in app.connection_handler.active_game:
        return {'status': 'The game already initialized'}

    game = app.connection_handler.start_game(request.remote_addr)
    return game.to_response()
