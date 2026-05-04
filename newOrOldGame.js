function selected(item){
    if(item.dataset.value === "new"){
        window.location.href = "difficulty_choosing.html";
    }else if(item.dataset.value === "old"){
        window.location.href = "index.html";
    }
}