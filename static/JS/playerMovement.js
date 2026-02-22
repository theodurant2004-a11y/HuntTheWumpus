function moveUp() {
    console.log("Le joueur monte !");
}

function moveDown() {
    console.log("Le joueur descend !");
}

function moveLeft() {
    console.log("Le joueur va à gauche !");
}

function moveRight() {
    console.log("Le joueur va à droite !");
}

document.addEventListener('keydown', (event) => {
    
    if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(event.key)) {
        event.preventDefault(); 
    }

    switch(event.key) {
        case "ArrowUp":
            moveUp();
            break;
        case "ArrowDown":
            moveDown();
            break;
        case "ArrowLeft":
            moveLeft();
            break;
        case "ArrowRight":
            moveRight();
            break;
    }
});