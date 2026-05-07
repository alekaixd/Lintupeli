fetch("http://localhost:3000/leaderboard")
    .then(response => response.json())
    .then(data => {

        const leaderboardDiv =
            document.getElementById("leaderboards_div");

        data.forEach(player => {

            leaderboardDiv.innerHTML += `
                <div class="bird">
                    <h1>${player.username}</h1>
                    <h2>${player.species}</h2>
                    <h2>${player.score}</h2>
                </div>
            `;
        });
    })
    .catch(error => {
        console.log("Error:", error);
    });

function Back(){
    window.location.href = "FinishScreen.html"
}