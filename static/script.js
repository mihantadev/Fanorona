document.addEventListener("DOMContentLoaded", function() {
    let selectedPiece = null;
    let placedPieces = 0;
    let currentPlayer = 1;

    document.querySelectorAll(".cell").forEach(cell => {
        cell.addEventListener("click", function() {
            let pos = parseInt(this.getAttribute("data-index"));

            fetch("/move", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ pos: pos, selected_piece: selectedPiece })
            })
            .then(response => response.json())
            .then(data => {
                updateBoard(data.etat_j1, data.etat_j2);
                currentPlayer = data.joueur;
                if (data.winner) {
                    document.querySelector(".result").innerText = `Le joueur ${data.winner} a gagné!`;
                }
            });
        });
    });

    function updateBoard(etat_j1, etat_j2) {
        document.querySelectorAll(".cell").forEach((cell, index) => {
            let mask = 1 << index;
            if (etat_j1 & mask) {
                cell.innerText = "O";
            } else if (etat_j2 & mask) {
                cell.innerText = "X";
            } else {
                cell.innerText = "";
            }
        });
    }

    function restartGame() {
    fetch('/reset', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        console.log("Jeu réinitialisé :", data);
        location.reload();  // Recharge la page pour afficher le nouveau plateau
    })
    .catch(error => console.error("Erreur lors de la réinitialisation :", error));
}
});
