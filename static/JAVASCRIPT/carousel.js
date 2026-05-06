// On attend que la page soit totalement chargée
document.addEventListener("DOMContentLoaded", function() {
    const options = document.querySelectorAll('.char-option');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    // Si on ne trouve pas d'avatars sur la page, on arrête le script
    if (options.length === 0) return;

    let currentIndex = 0;

    function updateCarousel() {
        // On cache tout et on décoche tout
        options.forEach(opt => {
            opt.classList.remove('active', 'prev', 'next');
            opt.querySelector('input').checked = false;
        });

        // On calcule les index (gauche, centre, droite)
        const total = options.length;
        const prevIndex = (currentIndex - 1 + total) % total;
        const nextIndex = (currentIndex + 1) % total;

        // On applique les bonnes classes
        options[prevIndex].classList.add('prev');
        options[currentIndex].classList.add('active');
        options[nextIndex].classList.add('next');

        // On coche le bouton radio caché de l'avatar au centre
        options[currentIndex].querySelector('input').checked = true;
    }

    // Fonction pour aller à gauche
    function moveLeft() {
        currentIndex = (currentIndex - 1 + options.length) % options.length;
        updateCarousel();
    }

    // Fonction pour aller à droite
    function moveRight() {
        currentIndex = (currentIndex + 1) % options.length;
        updateCarousel();
    }

    // Événements au clic sur les flèches (à l'écran)
    if (prevBtn) {
        prevBtn.addEventListener('click', moveLeft);
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', moveRight);
    }

    // ===========================
    //   NAVIGATION AU CLAVIER
    // ===========================
    document.addEventListener('keydown', function(event) {
        // Si l'utilisateur tape dans un champ de texte (login/password), on ne fait rien
        if (event.target.tagName === 'INPUT' && event.target.type !== 'radio') {
            return;
        }

        if (event.key === 'ArrowLeft') {
            moveLeft();
        } else if (event.key === 'ArrowRight') {
            moveRight();
        }
    });

    // On lance l'affichage initial
    updateCarousel();
});