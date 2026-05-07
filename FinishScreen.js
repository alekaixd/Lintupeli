function Leaderboard(){
    window.location.href = "leaderboards.html"
}

function Logout(){
    localStorage.clear();
    window.location.href = "game.html";
}

function SaveFinalGame() {

    document.getElementById("saveGameFinal")
        .style.pointerEvents = "none";

    var gameData = {
        score: localStorage.getItem("score"),
        gameId: localStorage.getItem("gameId"),
        userId: localStorage.getItem("user_id")
    };

    fetch("http://localhost:3000/saveFinalGame", {

        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(gameData)
    })

    .then(function (response) {
        return response.json();
    })

    .then(function (data) {

        var complaint =
            document.getElementById("complaint");

        if (data.success) {
            complaint.innerHTML = "Game saved successfully!";
        } else {
            complaint.innerHTML = "Could not save game!";
        }
    })

    .catch(function (error) {
        console.log(error);
        document.getElementById("complaint").innerHTML =
            "Server error!";
    });
}