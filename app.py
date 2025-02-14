from flask import Flask, render_template, request, jsonify, session
from game import Noeud

app = Flask(__name__)


# Initialisation du jeu
default_board = Noeud()
placed_pieces = 0  # Nombre de pièces placées

@app.route('/')
def index():
    global default_board
    default_board = Noeud()  # Réinitialisation à chaque nouvelle requête
    return render_template('index.html')


@app.route('/move', methods=['POST'])
def move():
    global default_board, placed_pieces

    data = request.json
    pos = data.get('pos')
    selected_piece = data.get('selected_piece')

    winner, placed_pieces = default_board.apply_move(pos, selected_piece, placed_pieces)

    return jsonify({
        "etat_j1": default_board.etat_j1,
        "etat_j2": default_board.etat_j2,
        "joueur": default_board.joueur_actuel,
        "winner": winner
    })

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('game_state', None)  # Supprime l'état du jeu stocké
    return jsonify({"message": "Jeu réinitialisé"})




if __name__ == '__main__':
    app.run(debug=True)
