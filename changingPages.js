const app = document.getElementById("app")

function ShowUserOptions(){
    app.innerHTML = `<header>
        <h1>Bird Game 🪽</h1>
    </header>

    <h1 id="text">Would you like to</h1>
    <div onclick="ShowLogin()" data-value="login" class="button">
        <h3>Login</h3>
    </div>
    <div onclick="ShowCreateUser()" data-value="create" class="button">
        <h3>Create user</h3>
    </div>`
}

function ShowLogin(){
    app.innerHTML = `<header>
        <h1>Bird Game 🪽</h1>
    </header>

    <div class="container">
        <h1>Login</h1>

        <h2>Username</h2>
        <input type="text" id="username">

        <h2>Password</h2>
        <input type="password" id="password">

        <button id="send" onclick="login()" class="user_padding">Login</button>

        <a href="#" onclick="ShowCreateUser()" class="user_padding">Don't have an account?</a>

        <p id="complaint"></p>
    </div>`
}

function ShowCreateUser(){
    app.innerHTML = `<header>
        <h1>Bird Game 🪽</h1>
    </header>
    <div class="container">
        <h1>Create user</h1>

        <h2>Username</h2>
        <input type="text" id="username">

        <h2>Password</h2>
        <input type="password" id="password">

        <button id="send" onclick="createUser()" class="user_padding">Create user</button>

        <a href="#" onclick="ShowLogin()" class="user_padding">Already have an account?</a>

        <p id="complaint"></p>
    </div>`
}

function ShowNewOrOldGame(){
    app.innerHTML = `<header>
        <h1>Bird Game 🪽</h1>
      </header>

      <div onclick="ShowNewGame()" data-value="new" class="button">
          <h3>Start new game</h3>
      </div>
      <div onclick="selected()" data-value="old" class="button">
          <h3>Continue previous game</h3>
      </div>`
}

function ShowNewGame(){
    app.innerHTML = `
      <header>
        <h1>Bird Game 🪽</h1>
      </header>

      <div onclick="clickedBird(this)" class="bird" data-name = "Eagle" data-max-energy = "50" id="Eagle">
        <img src="#" alt="">
        <h3>Eagle</h3>
        <p>Max energy: 50</p>
        <p>Difficulty: Easy</p>
      </div>

      <div onclick="clickedBird(this)" class="bird" data-name = "Raven" data-max-energy = "50" id="Raven">
        <img src="#" alt="">
        <h3>Raven</h3>
        <p>Max energy: 50</p>
        <p>Difficulty: Easy</p>
      </div>

      <div onclick="clickedBird(this)" class="bird" data-name = "Sparrow" data-max-energy = "40" id="Sparrow">
        <img src="#" alt="">
        <h3>Sparrow</h3>
        <p>Max energy: 40</p>
        <p>Difficulty: Medium</p>
      </div>

      <div onclick="clickedBird(this)" class="bird" data-name = "Hawk" data-max-energy = "40" id="Hawk">
        <img src="#" alt="">
        <h3>Hawk</h3>
        <p>Max energy: 40</p>
        <p>Difficulty: Medium</p>
      </div>

      <div onclick="clickedBird(this)" class="bird" data-name = "Owl" data-max-energy = "30" id="Owl">
        <img src="#" alt="">
        <h3>Owl</h3>
        <p>Max energy: 30</p>
        <p>Difficulty: Hard</p>
      </div>

      <div onclick="clickedBird(this)" class="bird" data-name = "Pigeon" data-max-energy = "30" id="Pigeon">
        <img src="#" alt="">
        <h3>Pigeon</h3>
        <p>Max energy: 30</p>
        <p>Difficulty: Hard</p>
      </div>

      <div onclick="ShowNewOrOldGame()" class="bird">
        <h3>Go back</h3>
      </div>`
}

function ShowOldGame(){
    app.innerHTML = `<body>
    <div id="elements"></div>
    </body>`
}

function ShowGame() {
    app.innerHTML = `
<div id="header">
        <header>
            <h1>Bird Game 🪽</h1>
            <nav>
                <ul>
                    <li>
                        <p id="username">User: </p>
                    </li>
                    <li>
                        <button id="infoBtn">Game Info</button>
                    </li>
                    <li>
                        <button id="audioToggleBtn">Mute Audio</button>
                    </li>
                    <li>
                        <button id="exit" onClick="logout()">Exit→</button>
                    </li>
                </ul>
            </nav>
        </header>

        <div id="header_line"></div>

        <div id="main_content">
            <div id="map"></div>

            <div id="control_panel">
                <div id="statsInfo">
                    <h2>Stats info:</h2>
                    <h3 id="mult">Multiplier: 2.0x</h3>
                    <p id="score">Total Score: 0</p>
                    <p id="energy">Energy: 50/50</p>
                    <p id="actions">Actions left: 3/3</p>
                    <p></p>
                </div>

                <div id="allBtn">
                    <button id="flyBtn">Fly</button>
                    <button id="eatBtn">Eat</button>
                    <button id="sleepBtn">Sleep</button>
                    <button id="chripBtn">Chirp</button>
                </div>

                <div id="flyOptions" className="hidden"></div>

                <div id="messageContainer" className="message hidden"></div>

                <div id="infoOverlay" className="hidden info-overlay">
                    <div className="info-box">
                        <h2>Information</h2>

                        <p>
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                            Vivamus lacinia odio vitae vestibulum vestibulum.
                            Cras venenatis euismod malesuada.
                        </p>

                        <button id="closeInfoBtn">Close</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `
}

window.onload = function() {
    ShowUserOptions();
};