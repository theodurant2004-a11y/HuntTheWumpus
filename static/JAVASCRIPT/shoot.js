let foundLostPanel = document.querySelector(".pannel"); 
let blockedInput = false;

if (foundLostPanel) {
    blockedInput = true;
}

document.addEventListener('keydown', (event) => {
    if (blockedInput) return;

    const key = event.key;
    const arrows = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"];

    if (key === "Space" || key === " ") {
        event.preventDefault();
        window.location.replace("/move/none");
        return;
    }

    if (arrows.includes(key)) {
        event.preventDefault();
        handleShoot(key);
    }
});

function handleShoot(key) {
    let direction = key.replace("Arrow", "").toLowerCase();
    window.location.replace("/shoot/" + direction);
}