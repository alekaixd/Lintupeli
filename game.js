
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
       iconSize:     [38, 95],
       shadowSize:   [50, 64],
       iconAnchor:   [22, 94],
       shadowAnchor: [4, 62],
       popupAnchor:  [-3, -76]
    }
});

var greenIcon = new LeafIcon({
    iconUrl: 'bird.png',
})

var marker = L.marker([0, 0], {icon: greenIcon}).addTo(map);
//////////////////////



let currentIcao = "EFIV"
let score = 0
let energy = 50
let maxEnergy = energy

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

async function SetFirstLocation() {
	url = "http://127.0.0.1:3000/start";
	try {
		const response = await fetch(url)
		if (!response.ok) {
			throw new Error("Response status: " + response.status)
		}

		const result = await response.json();
		marker.setLatLng([result["lat"], result["lon"]]);
		map.flyTo([result["lat"], result["lon"]], 5);
	}
	catch (error) {
		console.error(error.message);
	}
}

SetFirstLocation()

async function selectNextLocation(ICAO) {
	currentIcao = ICAO;
	url = "http://127.0.0.1:3000/fly/" + ICAO;
	flyOptions.innerHTML = "";
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
		for (let i = 0; i < Object.keys(result.Ports).length; i++) {
			const btn = document.createElement("button");
			flyOptions.appendChild(btn);
			btn.innerHTML = result["Ports"][i]["name"];
			btn.value = result["Ports"][i]["icao"]
			btn.addEventListener("click", () => {
				onControlClick("Option 1", () => {
					selectNextLocation(btn.value);
					restoreButtons();
				});
			});
		}
	}
	catch (error) {
		console.error(error.message);
	}
}

function restoreButtons() {
	flyOptions.classList.add("hidden");
	allButtons.classList.remove("hidden");
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
document.getElementById("sleepBtn").addEventListener("click", () => onControlClick("Sleep"));
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
		scoreText.innerHTML = "Score: " + score;
		onControlClick("Chirp")
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
		energy += result["addedEnergy"]
		energyText.innerHTML = "Energy: " + energy + "/" + maxEnergy;
		showMessage(result["message"])
	}
	catch (error) {
		console.error(error.message);
	}
}

function sleep() {
	energy = maxEnergy
	showMessage("You rested well! Energy fully restored")
}

const infoBtn = document.getElementById("infoBtn");
const infoOverlay = document.getElementById("infoOverlay");
const closeInfoBtn = document.getElementById("closeInfoBtn");

function openInfo() {
	infoOverlay.classList.remove("hidden");
}

function closeInfo() {
	infoOverlay.classList.add("hidden");
}

infoBtn.addEventListener("click", openInfo);
closeInfoBtn.addEventListener("click", closeInfo);

async function logout() {
	const response = await fetch("http://localhost:3000/logout", {
		method: "POST"
	});

	const data = await response.json();

	if (data.success) {
		window.location.href = "userOptions.html";
	}
}
