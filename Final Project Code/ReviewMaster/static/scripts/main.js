const homeClass = document.querySelector(".home");
const loginClass = document.querySelector(".login");

if (homeClass || loginClass) {
    document.getElementsByClassName("header__search")[0].style.display = "none";
}

const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
    dropdownButton.style.transform = dropdownMenu.classList.contains("show") ? 'rotate(180deg)' : 'rotate(0deg)';
    dropdownButton.style.paddingTop = dropdownMenu.classList.contains("show") ? '0' : '.25rem';
  });
}