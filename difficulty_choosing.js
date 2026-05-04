async function clickedBird(element){
      let info = {
        name: element.dataset.name,
        maxEnergy: Number(element.dataset.maxEnergy)
      };

    console.log(info);

    const response = await fetch("http://127.0.0.1:3000/difficulty", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(info)
    });

    const data = await response.json();
    console.log("server response:", data)

    if (data.success){
        window.location.href = "index.html"
    }

}

function selected(){
    window.location.href = "newOrOldGame.html";
}