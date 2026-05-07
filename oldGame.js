async function oldGames() {
    try {
        const userId = localStorage.getItem("user_id");

        const response = await fetch(`http://127.0.0.1:3000/oldGameData?userId=${userId}`);
        const games = await response.json();

        const container = document.getElementById("elements");
        container.innerHTML = "";

        games.forEach(game => {
            const card = document.createElement("div");
            card.classList.add("game-card");

            card.innerHTML = `
                <div class="bird">
                <h3>${game.species_name}</h3>
                <p>Score: ${game.score}</p>
                <p>Energy: ${game.current_energy} / ${game.max_energy}</p>
                <p>Location: ${game.location}</p>
                </div>
            `;

            card.addEventListener("click", () => {
                selectGame(game);
            });

            container.appendChild(card);
        });

    } catch (error) {
        console.error("Error: ", error);
    }
}

function selectGame(game) {
    const saveData = {
        species_name: game.species_name,
        score: game.score,
        current_energy: game.current_energy,
        max_energy: game.max_energy,
        location: game.location,
        id: game.id
    };

    localStorage.setItem("selected_game", JSON.stringify(saveData));

    window.location.href = "index.html";
}

document.addEventListener("DOMContentLoaded", oldGames);
