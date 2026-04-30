let foundTriggeredBat = document.querySelector(".triggered_bat");
let foundLostPanel = document.querySelector(".pannel"); 
let blockedMovement = false;
let firemode = false;

if (foundTriggeredBat) {
    blockedMovement = true;
    setTimeout(function() {
        window.location.replace("/move/none");
    }, 1000);
}

if (foundLostPanel) {
    blockedMovement = true;
}

document.addEventListener('keydown', (event) => {
    if (blockedMovement) return;

    const key = event.key;
    const arrows = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"];

    if (key === "Space" || key === " ") {
        event.preventDefault();
        firemode = !firemode;
        console.log("Fire mode:", firemode ? "ON" : "OFF");
        //changer l'interface pour qu'on comprenne qu'on est en firemode
        return;
    }

    if (arrows.includes(key)) {
        event.preventDefault();

        if (firemode) {
            handleShoot(key);
        } else {
            handleMove(key);
        }
    }
});

function handleMove(key) {
    switch(key) {
        case "ArrowUp":    window.location.replace("/move/up"); break;
        case "ArrowDown":  window.location.replace("/move/down"); break;
        case "ArrowLeft":  window.location.replace("/move/left"); break;
        case "ArrowRight": window.location.replace("/move/right"); break;
    }
}

function handleShoot(key) {
    let direction = key.replace("Arrow", "").toLowerCase();
    console.log("Tir déclenché vers : " + direction);
    
    // mettre la mécanique de tir
    // window.location.replace("/shoot/" + direction);
}