function selected(item){
    if(item.dataset.value === "login"){
        window.location.href = "login.html";
    } else if(item.dataset.value === "create"){
        window.location.href = "createUser.html";
    }
}