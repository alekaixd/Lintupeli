function Save() {
    let selectedGame = JSON.parse(localStorage.getItem("selected_game"));

    let gameId = null;

    if (selectedGame) {
        gameId = selectedGame.id;
    }

    const data = {
        userId: localStorage.getItem("userId"),
        currentIcao: localStorage.getItem("currentIcao"),
        currentEnergy: localStorage.getItem("currentEnergy"),
        maxEnergy: localStorage.getItem("maxEnergy"),
        score: localStorage.getItem("score"),
        gameId: gameId
    };

    fetch("http://127.0.0.1:3000/saveGame", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
        })
    .then(function (res) {
        return res.json();
    })
    .then(function (data) {
        if (data.success) {
            document.getElementById("alert").innerText = "Game saved!";
        } else {
            document.getElementById("alert").innerText = "Save failed!";
        }
    })
    .catch(function (err) {
        console.error(err);
        document.getElementById("alert").innerText = "Error saving game!";
    });
}

function Exit(){
    localStorage.clear();
    window.location.href = "game.html";
}