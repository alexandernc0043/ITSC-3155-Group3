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
    dropdownButton.style.transform = dropdownMenu.classList.contains("show")
      ? "rotate(180deg)"
      : "rotate(0deg)";
    dropdownButton.style.paddingTop = dropdownMenu.classList.contains("show")
      ? "0"
      : ".25rem";
  });
}

const alertMessages = document.querySelector(".alert-messages");

if (alertMessages) {
  const liElement = alertMessages.getElementsByTagName("li");
  const classList = liElement[0].classList;
  if (classList.contains("error")) {
    alertMessages.classList.add("error");
  } else if (classList.contains("success")) {
    alertMessages.classList.add("success");
  }
}

const input = document.querySelector(".header__search input");
const removeInput = document.querySelector(".clear-input-button");

if (input.value) {
  removeInput.classList.add("show");
}

removeInput.addEventListener("click", () => {
  input.value = "";
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

// Shows/Hides password form depending on user option
var option = document.getElementById("id_option");

function showPasswordForm() {
  const container = document.getElementById("container");
  var fields = document.querySelectorAll(
    "#id_old_password, #id_new_password1, #id_new_password2"
  );

  if (option.value === "no") {
    container.style.display = "none";
    fields.forEach((field) => {
      field.removeAttribute("required");
    });
  } else {
    container.style.display = "block";
    fields.forEach((field) => {
      field.setAttribute("required", "");
      field.value = "";
    });
  }
}

option.addEventListener("change", showPasswordForm);
