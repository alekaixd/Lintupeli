function createUser() {
        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;

        fetch("http://127.0.0.1:3000/createUser", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({
                username: username,
                password: password
            })

        })

        .then(response => response.json())

        .then(data => {
            if (data.success) {
                window.location.href = "newOrOldGame.html";
            } else {
                document.getElementById("complaint").innerText = data.message;
            }
        })

        .catch(error => console.error(error));
}