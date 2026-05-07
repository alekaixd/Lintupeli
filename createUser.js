function createUser() {
        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;

        fetch("http://localhost:3000/createUser", {
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
            if (data.success) {
                localStorage.setItem("user_id", data.player_id);
                localStorage.setItem("username", data.username)

                ShowNewOrOldGame()
            } else {
                document.getElementById("complaint").innerText = data.message;
            }
        })

        .catch(error => console.error(error));
}