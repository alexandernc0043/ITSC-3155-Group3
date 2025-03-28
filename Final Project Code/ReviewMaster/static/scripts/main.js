const homeClass = document.getElementsByClassName("home");
const loginClass = document.getElementsByClassName("login");

if (homeClass || loginClass) {
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

if (alertMessages) {
  const liElement = alertMessages.getElementsByTagName("li");
  const classList = liElement[0].classList;
  if (classList.contains("error")) {
    alertMessages.classList.add("error");
  }
  else if (classList.contains("success")) {
    alertMessages.classList.add("success");
  }
}

const input = document.querySelector(".header__search input");
const removeInput = document.querySelector(".clear-input-button");

if (input.value) {
  removeInput.classList.add("show");
}

removeInput.addEventListener("click", () => {
  input.value = '';
  input.focus();
  removeInput.classList.remove("show");
});

input.addEventListener("input", (e) => {
  if (e.target.value && !input.classList.contains("show")) {
    removeInput.classList.add("show");
  } else if (!e.target.value && input.classList.contains("show")) {
    removeInput.classList.remove("show");
  }
});