import numpy as np
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

def generate_board():
    """Génère une configuration aléatoire de Fanorona Telo."""
    board = [0] * 9  # 9 intersections (0 = vide, 1 = blanc, -1 = noir)
    white_positions = random.sample(range(9), 3)
    black_positions = random.sample([p for p in range(9) if p not in white_positions], 3)
    for pos in white_positions:
        board[pos] = 1
    for pos in black_positions:
        board[pos] = -1
    return board

def is_winning(board, player=1):
    """Vérifie si un joueur a gagné."""
    winning_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Lignes horizontales
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colonnes
        [0, 4, 8], [2, 4, 6]  # Diagonales
    ]
    return any(all(board[i] == player for i in pattern) for pattern in winning_patterns)

def generate_dataset(n_wins=500, n_losses=500):
    """Génère un dataset de configurations gagnantes et perdantes."""
    data = []
    labels = []
    while len(data) < n_wins + n_losses:
        board = generate_board()
        if len(data) < n_wins and is_winning(board, 1):
            data.append(board)
            labels.append(1)  # 1 = victoire blanche
        elif len(data) >= n_wins and is_winning(board, -1):
            data.append(board)
            labels.append(0)  # 0 = défaite blanche
    return np.array(data), np.array(labels)

# Génération du dataset
data, labels = generate_dataset()

# Séparation en train/test
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Modèle 1 : Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
print("Random Forest Performance:")
print(classification_report(y_test, y_pred_rf))

# Modèle 2 : SVM
svm = SVC(kernel='linear')
svm.fit(X_train, y_train)
y_pred_svm = svm.predict(X_test)
print("\nSVM Performance:")
print(classification_report(y_test, y_pred_svm))

# Comparaison des scores
rf_acc = accuracy_score(y_test, y_pred_rf)
svm_acc = accuracy_score(y_test, y_pred_svm)
print(f"\nRandom Forest Accuracy: {rf_acc:.4f}")
print(f"SVM Accuracy: {svm_acc:.4f}")
