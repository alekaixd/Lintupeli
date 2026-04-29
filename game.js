
//mapbox
var map = L.map("map").setView([0, 0], 1);

L.tileLayer(
	"https://api.maptiler.com/maps/hybrid-v4/256/{z}/{x}/{y}.png?key=hgRLL8HKqMgdmq7CmhzW",
	{
		attribution:
			'<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
	},
).addTo(map);

const locations = [
	{ lat: 40.7128, lng: -74.006 }, // New York
	{ lat: 34.0522, lng: -118.2437 }, // Los Angeles
	{ lat: 51.5074, lng: -0.1278 }, // London
	{ lat: 48.8566, lng: 2.3522 }, // Paris
	{ lat: 35.6762, lng: 139.6503 }, // Tokyo
	{ lat: -33.8688, lng: 151.2093 }, // Sydney
	{ lat: 55.7558, lng: 37.6173 }, // Moscow
	{ lat: 19.4326, lng: -99.1332 }, // Mexico City
	{ lat: 39.9042, lng: 116.4074 }, // Beijing
	{ lat: -23.5505, lng: -46.6333 }, // São Paulo
];

let currentIcao = "EFIV"

let currentIndex = 0;
var marker = L.marker([locations[currentIndex].lat, locations[currentIndex].lng]).addTo(map);

const allButtons = document.getElementById("allBtn");
const flyOptions = document.getElementById("flyOptions");
const flyBtn = document.getElementById("flyBtn");
const option1Btn = document.getElementById("option1Btn");
const option2Btn = document.getElementById("option2Btn");

function selectNextLocation(ICAO) {
	if (currentIndex < locations.length - 1) {
		currentIndex++;
		const location = locations[currentIndex];
		map.setView([location.lat, location.lng], 10);
		marker.setLatLng([location.lat, location.lng]);
		flyOptions.innerHTML = ""
		currentIcao = ICAO
	} else {
		alert("You reached the end.");
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
		console.log(result)
		for (let i = 0; i < result.length; i++) {
			const btn = document.createElement("button")
			flyOptions.appendChild(btn)
			btn.innerHTML = result[i] // todo: get name from db
			btn.value = result[i]
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
document.getElementById("eatBtn").addEventListener("click", () => onControlClick("Eat"));
document.getElementById("sleepBtn").addEventListener("click", () => onControlClick("Sleep"));
document.getElementById("chripBtn").addEventListener("click", () => onControlClick("Chirp"));

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

