from flask import Flask, request, render_template, redirect, url_for
from core.connection_handler import ConnectionHandler

app = Flask(__name__)
app.connection_handler = ConnectionHandler()


# Used for testing specific features
app.config['TESTING'] = True


@app.route('/')
def index():
    """
    :return: return the front-end index
    """
    return render_template('index.html')


@app.route('/game_state')
def get_game_state():
    return app.connection_handler.get_last_result()


@app.route('/start_game', methods=['GET'])
def start_game():
    """
    :return: representation of a new game if two player are connected,
    other message describing the state otherwise.
    """
    if app.connection_handler.is_first_game_request():
        app.connection_handler.wait_for_second_player(request.remote_addr)
        result = {'status': 'Waiting For Second Player'}

    elif not app.config['TESTING'] and app.connection_handler.is_same_connection(request.remote_addr):
        # we don't want to update this as a new state
        return {'status': 'The same player entered twice'}

    elif app.connection_handler.game_started():
        result = {'status': 'The game already initialized'}

    else:
        game = app.connection_handler.start_game(request.remote_addr)
        result = game.to_response()

    app.connection_handler.update_last_result(result)
    return result


@app.route('/restart_game', methods=['GET'])
def restart_game():
    app.connection_handler.restart_game()
    return redirect('/')

