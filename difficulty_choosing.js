function clickedBird(element){
    let info = {
        name: element.dataset.name,
        maxEnergy: Number(element.dataset.maxEnergy)
    };

    console.log(info);

    localStorage.setItem("bird_name", info.name);
    localStorage.setItem("max_energy", info.maxEnergy);

    window.location.href = "index.html";
}