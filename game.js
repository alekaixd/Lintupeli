
//mapbox



var map = L.map("map").setView([0, 0], 1);

L.tileLayer(
	"https://api.maptiler.com/maps/hybrid-v4/256/{z}/{x}/{y}.png?key=hgRLL8HKqMgdmq7CmhzW",
	{
		attribution:
			'<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
	},
).addTo(map);



//creating new icon for marker
var LeafIcon = L.Icon.extend({
	options: {
		iconSize: [38, 95],
		shadowSize: [50, 64],
		iconAnchor: [22, 94],
		shadowAnchor: [4, 62],
		popupAnchor: [-3, -76]
	}
});

var greenIcon = new LeafIcon({
	iconUrl: 'bird.png',
});

var marker = L.marker([0, 0], { icon: greenIcon }).addTo(map);
//////////////////////

const username = localStorage.getItem("username")

function GetInitialGameState() {
	const gameRaw = localStorage.getItem("selected_game");
	const game = gameRaw ? JSON.parse(gameRaw) : null;

	const birdName = localStorage.getItem("bird_name");
	const birdMaxEnergyRaw = localStorage.getItem("max_energy");
	const birdMaxEnergy = birdMaxEnergyRaw ? Number(birdMaxEnergyRaw) : null;

	let speciesName;
	if (game && game.species_name != null) {
		speciesName = game.species_name;
	} else if (birdName != null) {
		speciesName = birdName;
	} else {
		speciesName = "Unknown Bird";
	}

	let maxEnergy;
	if (game && game.max_energy != null) {
		maxEnergy = game.max_energy;
	} else if (birdMaxEnergy != null) {
		maxEnergy = birdMaxEnergy;
	} else {
		maxEnergy = 50;
	}

	let energy;
	if (game && game.current_energy != null) {
		energy = game.current_energy;
	} else if (birdMaxEnergy != null) {
		energy = birdMaxEnergy;
	} else {
		energy = 50;
	}

	let score;
	if (game && game.score != null) {
		score = game.score;
	} else {
		score = 0;
	}

	let location;
	if (game && game.location != null) {
		location = game.location;
	} else {
		location = "EFIV";
	}

	return {
		speciesName,
		maxEnergy,
		energy,
		score,
		location
	};
}

const state = GetInitialGameState();

let speciesName = state.speciesName;
let maxEnergy = state.maxEnergy;
let energy = state.energy;
let score = state.score;
let currentIcao = state.location;

console.log(speciesName)
console.log(maxEnergy)
console.log(energy)
console.log(score)
console.log(currentIcao)

/*
let currentIcao = "EFIV";
let score = 0;
let maxEnergy = localStorage.getItem("max_energy");
if (maxEnergy == null) {
	maxEnergy = 50
}
let energy = maxEnergy;
*/
let combo = 1;
let maxActions = 3;
let actions = maxActions;

const uid = localStorage.getItem("user_id")
console.log(uid)

const allButtons = document.getElementById("allBtn");
const flyOptions = document.getElementById("flyOptions");
const flyBtn = document.getElementById("flyBtn");
const option1Btn = document.getElementById("option1Btn");
const option2Btn = document.getElementById("option2Btn");
const usernameText = document.getElementById("username");
const multiplierText = document.getElementById("mult");
const scoreText = document.getElementById("score");
const energyText = document.getElementById("energy");
const actionText = document.getElementById("actions");

updateEnergy();
scoreText.innerHTML = "🌟 Total Score: " + score;

async function SetFirstLocation() {
	if (currentIcao == null) {

		url = "http://127.0.0.1:3000/start";
		try {
			const response = await fetch(url);
			if (!response.ok) {
				throw new Error("Response status: " + response.status);
			}

			const result = await response.json();
			marker.setLatLng([result["lat"], result["lon"]]);
			map.flyTo([result["lat"], result["lon"]], 5);
		}
		catch (error) {
			console.error(error.message);
		}
	}
	else {
		selectNextLocation(currentIcao)
	}
}

SetFirstLocation()

async function selectNextLocation(ICAO) {
	url = "http://127.0.0.1:3000/fly/" + ICAO + "?currentICAO=" + currentIcao + "&combo=" + combo;
	currentIcao = ICAO;
	try {
		const response = await fetch(url)
		if (!response.ok) {
			throw new Error("Response status: " + response.status)
		}

		const result = await response.json();
		console.log(result["lat"]);
		console.log(result["lon"]);
		marker.setLatLng([result["lat"], result["lon"]]);
		map.setView([result["lat"], result["lon"]], 7);

		score += result["gainedScore"];
		scoreText.innerHTML = "🌟 Total Score: " + score;
		energy -= result["energyUsed"];
		updateEnergy();
		combo += 1;
		actions = maxActions
		updateActions()
		updateCombo()
	}
	catch (error) {
		console.error(error.message);
	}

}

async function showFlyOptions() {
	allButtons.classList.add("hidden");
	flyOptions.classList.remove("hidden");
	showMessage("You choose option \"Fly\"");
	url = "http://127.0.0.1:3000/map/" + currentIcao;
	try {
		const response = await fetch(url);
		if (!response.ok) {
			throw new Error("Response status: " + response.status);
		}

		const result = await response.json();
		if (Object.keys(result.Ports).length != 0) {

			for (let i = 0; i < Object.keys(result.Ports).length; i++) {
				const btn = document.createElement("button");
				flyOptions.appendChild(btn);
				btn.id = "confirmFlyBtn"
				btn.innerHTML = result["Ports"][i]["name"] + "<br>" + result["Ports"][i]["distance"] + "km";
				btn.value = result["Ports"][i]["icao"]
				btn.addEventListener("click", () => {
					onControlClick("Option 1", () => {
						selectNextLocation(btn.value);
						restoreButtons();
					});
				});
			};
			const backBtn = document.createElement("button");
			flyOptions.appendChild(backBtn);
			backBtn.innerHTML = "Back";
			backBtn.addEventListener("click", () => {
				restoreButtons();
			});
		}
		else {
			openInfo("You Migrated successfully!", "Remember to enjoy your summer vacation :D")
			//you win
		}
	}
	catch (error) {
		console.error(error.message);
	}
}

function restoreButtons() {
	flyOptions.classList.add("hidden");
	allButtons.classList.remove("hidden");
	flyOptions.innerHTML = "";
}

function showMessage(text) {
	const messageContainer = document.getElementById("messageContainer");
	messageContainer.textContent = text;
	window.clearTimeout(messageContainer.dataset.timeout);

	// Reset the element to full opacity immediately before fading again.
	messageContainer.style.transition = "none";
	messageContainer.classList.remove("hidden", "fade-out", "visible-message");
	messageContainer.offsetWidth;
	messageContainer.classList.add("visible-message");
	messageContainer.style.transition = "opacity 10s linear";

	requestAnimationFrame(() => {
		messageContainer.classList.remove("visible-message");
		messageContainer.classList.add("fade-out");
	});

	messageContainer.dataset.timeout = window.setTimeout(() => {
		messageContainer.classList.add("hidden");
		messageContainer.classList.remove("fade-out", "visible-message");
		messageContainer.style.transition = "opacity 10s linear";
	}, 10000);
}

function onControlClick(buttonName, action) {
	showMessage(`You choose option \"${buttonName}\"`);
	if (action) action();
}

flyBtn.addEventListener("click", () => onControlClick("Fly", showFlyOptions));

/*
option1Btn.addEventListener("click", () => {
	onControlClick("Option 1", () => {
		selectNextLocation();
		restoreButtons();
	});
});
option2Btn.addEventListener("click", () => {
	onControlClick("Option 2", () => {
		selectNextLocation();
		restoreButtons();
	});
});
*/
document.getElementById("eatBtn").addEventListener("click", () => Eat());
document.getElementById("sleepBtn").addEventListener("click", () => sleep());
document.getElementById("chripBtn").addEventListener("click", () => Chirp());

async function Chirp() {
	url = "http://127.0.0.1:3000/chirp";
	try {
		const response = await fetch(url);
		if (!response.ok) {
			throw new Error("Response status: " + response.status);
		}

		const result = await response.json();
		score += result["addedScore"];
		actions -= 1;
		combo = 1;
		updateCombo()
		updateActions();
		scoreText.innerHTML = "🌟 Score: " + score;
		onControlClick("Chirp");
	}
	catch (error) {
		console.error(error.message);
	}
}

async function Eat() {
	url = "http://127.0.0.1:3000/eat";
	try {
		const response = await fetch(url);
		if (!response.ok) {
			throw new Error("Response status: " + response.status);
		}

		const result = await response.json();
		maxEnergy += result["addedEnergy"];
		energy += result["addedEnergy"];
		actions -= 1;
		combo = 1;
		updateCombo()
		updateActions()
		updateEnergy();
		showMessage(result["message"]);
	}
	catch (error) {
		console.error(error.message);
	}
}

function sleep() {
	energy = maxEnergy;
	actions -= 1;
	combo = 1;
	updateCombo()
	updateActions();
	updateEnergy();
	showMessage("You rested well! Energy fully restored");
}

const infoBtn = document.getElementById("infoBtn");
const infoOverlay = document.getElementById("infoOverlay");
const closeInfoBtn = document.getElementById("closeInfoBtn");
const infoTitle = document.getElementById("infoTitle")
const infoText = document.getElementById("infoText")

function openInfo(title, text) {
	infoOverlay.classList.remove("hidden");
	infoTitle.innerHTML = title
	infoText.innerHTML = text
}

function closeInfo() {
	infoOverlay.classList.add("hidden");
}

const iTitle = "Migration Migraine"
const iText = "You are a bird trying to survive the deadly winter.\nManage your energy wisely to reach your vacation home for the winter.Eat food to raise your maximum energy and sleep to recharge all of your energy."
openInfo(iTitle, iText);
infoBtn.addEventListener("click", function infoEvent() {
	openInfo(iTitle, iText);
});
closeInfoBtn.addEventListener("click", closeInfo);
infoOverlay.addEventListener("click", function(event) {
	if (event.target === infoOverlay) {
		closeInfo();
	}
});

async function logout() {
	const response = await fetch("http://localhost:3000/logout", {
		method: "POST"
	});

	const data = await response.json();

	if (data.success) {
		window.location.href = "userOptions.html";
	}
}

function updateEnergy() {
	if (energy <= 0) {
		energy = 0
		energyText.innerHTML = "⚡ Energy: " + energy + "/" + maxEnergy;
		openInfo("You lose!", "You ran out of energy. Remember to sleep and eat to gain more energy<br>Your Score: " + score)
	}
	else {
		energyText.innerHTML = "⚡ Energy: " + energy + "/" + maxEnergy;
	}
}

function updateActions() {
	actionText.innerHTML = "🔥 Actions: " + actions + "/" + maxActions;
	if (actions < 0) {
		openInfo("You lose!", "You stayed still too long. Fly more often so the winter doesnt catch up to you<br>Your Score: " + score)
	}
}

function updateCombo() {
	multiplierText.innerHTML = "⭐ Multiplier: " + combo + "x"
}

function options() {
	window.location.href = "savexit.html";
}
