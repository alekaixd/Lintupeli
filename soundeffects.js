const hoverSound = new Audio('hover.mp3');
const clickSound = new Audio('click.mp3');
const closeSound = new Audio('close.mp3');

hoverSound.volume = 0.35;
clickSound.volume = 0.35;
closeSound.volume = 0.95;

let audioEnabled = true;
const audioToggleBtn = document.getElementById('audioToggleBtn');

function updateAudioToggleButton() {
	if (!audioToggleBtn) return;
	audioToggleBtn.textContent = audioEnabled ? 'Mute Audio' : 'Unmute Audio';
}

function playSound(audio, force = false) {
	if (!audio || (!audioEnabled && !force)) return;
	audio.currentTime = 0;
	audio.play().catch(() => {
		// Ignore playback errors from browser autoplay policies.
	});
}

function toggleAudio() {
	playSound(clickSound, true);
	audioEnabled = !audioEnabled;
	updateAudioToggleButton();
}

if (audioToggleBtn) {
	audioToggleBtn.addEventListener('click', toggleAudio);
}

function handleButtonHover(event) {
	const button = event.target.closest('button');
	if (!button) return;

	if (event.relatedTarget && button.contains(event.relatedTarget)) {
		return;
	}

	playSound(hoverSound);
}

function handleButtonClick(event) {
	const button = event.target.closest('button');
	if (!button) return;

	if (button.id === 'closeInfoBtn') {
		playSound(closeSound);
	} else if (button.id !== 'audioToggleBtn') {
		playSound(clickSound);
	}
}

document.addEventListener('mouseover', handleButtonHover);
document.addEventListener('click', handleButtonClick);
