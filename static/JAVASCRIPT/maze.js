let foundTriggeredBat = document.querySelector(".triggered_bat");
let blockedMovement = false;

if(foundTriggeredBat){
    blockedMovement = true
    setTimeout(function() {
        window.location.replace("/Maze");
    }, 1000);
}
else{
    blockedMovement = false;
}

document.addEventListener('keydown', (event) => {
    if (blockedMovement == false){
        if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(event.key)) {
            event.preventDefault(); 
        }

        switch(event.key) {
            case "ArrowUp":
                window.location.replace("/move/up");
                break;
            case "ArrowDown":
                window.location.replace("/move/down");
                break;
            case "ArrowLeft":
                window.location.replace("/move/left");
                break;
            case "ArrowRight":
                window.location.replace("/move/right");
                break;
        }
    }    
});