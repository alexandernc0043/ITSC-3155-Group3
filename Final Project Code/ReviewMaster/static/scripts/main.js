const homeClass = document.getElementsByClassName("home");
const loginClass = document.getElementsByClassName("login");

if (homeClass.length > 0) {
  document.getElementsByClassName("header__search")[0].style.display = "none";
}

if (loginClass.length > 0) {
  document.getElementsByClassName("header__search")[0].style.display = "none";
}

// Hide password form on dropdown option

function showForm() {
  var choice = document.getElementById("select");
  const container = document.getElementById("container");
  var choices = document.querySelectorAll("#id_old_password, #id_new_password1, #id_new_password2");

  if (choice.selectedIndex == 0) {
    container.style.display = "none";
    choices.forEach((field) => {
      field.removeAttribute("required");
    });
  } else {
    container.style.display = "block";
    choices.forEach((field) => {
      field.setAttribute("required", "");
    });
  }
}

window.onload = showForm();
