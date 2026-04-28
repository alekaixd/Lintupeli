const button = document.getElementById("send");
button.addEventListener('click', function(){
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })

    })

    .then(response => response.json())

    .then(data => {
        if(data.success){
            window.location.href = "/";
        } else {
            document.getElementById("complaint").innerText = "wrong username or password";
        }
    })

    .catch(error => console.error(error))
})