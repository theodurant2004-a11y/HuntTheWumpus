document.addEventListener('keydown', (event) => {
    if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(event.key)) {
        event.preventDefault(); 
    }

    switch(event.key) {
        case "ArrowUp":
            window.location.href = "/move/up";
            break;
        case "ArrowDown":
            window.location.href = "/move/down";
            break;
        case "ArrowLeft":
            window.location.href = "/move/left";
            break;
        case "ArrowRight":
            window.location.href = "/move/right";
            break;
    }
});