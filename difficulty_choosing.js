async function clickedBird(element){
      let info = {
        name: element.dataset.name,
        maxEnergy: Number(element.dataset.maxEnergy)
      };

    console.log(info);

    const response = await fetch("http://localhost:3000/difficulty", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(info)
    });

    const data = await response.json();
    console.log("server response:", data)

    if (data.success){
        ShowGame()
    }

}