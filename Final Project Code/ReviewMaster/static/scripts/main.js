const homeClass = document.getElementsByClassName("home");
const loginClass = document.getElementsByClassName("login");
const dropdownButton = document.getElementsByClassName('dropdown-button')[0]
const dropdownMenu = document.getElementsByClassName('dropdown-menu')[0]

dropdownMenu.style.display = 'none';
dropdownButton.addEventListener('click', () => {
    if (dropdownMenu.style.display === 'none') {
        dropdownMenu.style.display = 'block';
        dropdownButton.style.transform = 'rotateX(180deg)';
    } else {
        dropdownMenu.style.display = 'none';
        dropdownButton.style.transform = 'rotateX(0deg)';
    }
});

if (homeClass.length > 0) {
    document.getElementsByClassName("header__search")[0].style.display = "none";
}

if (loginClass.length > 0) {
    document.getElementsByClassName("header__search")[0].style.display = "none";
}
