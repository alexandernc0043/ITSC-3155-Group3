const homeClass = document.getElementsByClassName("home");
const loginClass = document.getElementsByClassName("login");

if (homeClass.length > 0 || loginClass.length > 0) {
    document.getElementsByClassName("header__search")[0].style.display = "none";
}
