document.addEventListener('DOMContentLoaded', () => {
    
    // ===================================
    //      GESTION DU LECTEUR AUDIO 
    // ===================================
    const music = document.getElementById('bg-music');
    
    if (music) {
        const savedVolume = localStorage.getItem("game_volume") || 0.2;
        const currentTrack = music.querySelector("source").src;
        const savedTime = sessionStorage.getItem("musicTime");
        const savedTrack = sessionStorage.getItem("musicTrack");

        music.volume = savedVolume;

        if (savedTime && savedTrack === currentTrack) {
            music.currentTime = parseFloat(savedTime);
        }

        window.addEventListener("beforeunload", () => {
            sessionStorage.setItem("musicTime", music.currentTime);
            sessionStorage.setItem("musicTrack", currentTrack);
        });
    }

    // =======================
    //      GESTION CURSEUR 
    // =======================
    const slider = document.getElementById('volume-slider');
    const volDisplay = document.getElementById('volume-val');

    if (slider && volDisplay && music) {
        
        slider.value = music.volume;
        volDisplay.innerText = Math.round(slider.value * 100) + "%";

        slider.addEventListener('input', function() {
            const val = this.value;
            music.volume = val;
            volDisplay.innerText = Math.round(val * 100) + "%";
            
            localStorage.setItem("game_volume", val);
        });
    }
});