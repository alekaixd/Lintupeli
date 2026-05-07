async function oldGames(){
    try{
        const response = await fetch("http://127.0.0.1:3000/oldGameData", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("token")
            }
        })

        const games = await response.json();

        console.log(games);

        for (game of games){
            document.getElementById("elements").innerHTML += "<h3>" + game.species_name + "</h3>"
        }

    } catch (error) {
        console.error("Error: ", error);
    }
}


document.addEventListener("DOMContentLoaded", function(){
    oldGames();
})