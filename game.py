class Noeud:
    ALIGNMENTS = [
        0b111000000, 0b000111000, 0b000000111,  # Lignes
        0b100100100, 0b010010010, 0b001001001,  # Colonnes
        0b100010001, 0b001010100               # Diagonales
    ]
    
    def __init__(self, etat_j1=0, etat_j2=0, joueur_actuel=1):
        self.etat_j1 = etat_j1
        self.etat_j2 = etat_j2
        self.joueur_actuel = joueur_actuel

    def get_valid_moves(self, index):
        """Retourne les déplacements valides à partir de la position index."""
        voisins = [
            [1, 3, 4], [0, 2, 4], [1, 4, 5],
            [0, 4, 6], [0, 1, 2, 3, 5, 6, 7, 8], [2, 4, 8],
            [3, 4, 7], [4, 6, 8], [4, 5, 7]
        ]
        return [pos for pos in voisins[index] if not ((1 << pos) & (self.etat_j1 | self.etat_j2))]

    def check_winner(self):
        """Vérifie si un joueur a gagné."""
        for align in self.ALIGNMENTS:
            if (self.etat_j1 & align) == align:
                return 1
            if (self.etat_j2 & align) == align:
                return 2
        return None

    def apply_move(self, pos, selected_piece, placed_pieces):
        """Applique un coup au plateau."""
        if placed_pieces < 6:  # Phase de placement
            if not (self.etat_j1 | self.etat_j2) & (1 << pos):
                if self.joueur_actuel == 1:
                    self.etat_j1 |= (1 << pos)
                else:
                    self.etat_j2 |= (1 << pos)
                placed_pieces += 1
                self.joueur_actuel = 3 - self.joueur_actuel
        else:  # Phase de déplacement
            if selected_piece is not None and pos in self.get_valid_moves(selected_piece):
                if self.joueur_actuel == 1:
                    self.etat_j1 &= ~(1 << selected_piece)
                    self.etat_j1 |= (1 << pos)
                else:
                    self.etat_j2 &= ~(1 << selected_piece)
                    self.etat_j2 |= (1 << pos)
                self.joueur_actuel = 3 - self.joueur_actuel
        return self.check_winner(), placed_pieces
