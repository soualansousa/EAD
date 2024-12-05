function checkScreenWidth() {
    const navDesktop = document.querySelector('.navDesktop');
    const navMob = document.querySelector('.navMob');
    
    if (window.innerWidth <= 815) {
        navDesktop.classList.add('disable');
        navMob.classList.remove('disable');
    } else {
        navDesktop.classList.remove('disable');
        navMob.classList.add('disable');
    }
}

checkScreenWidth();

window.addEventListener('resize', checkScreenWidth);