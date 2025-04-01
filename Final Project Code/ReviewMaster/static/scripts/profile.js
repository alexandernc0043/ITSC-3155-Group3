// Shows/Hides password form depending on user option
const changePasswordButton = document.getElementById("change-password");
const container = document.getElementById("container");
const fields = document.querySelectorAll(
    "#id_old_password, #id_new_password1, #id_new_password2"
);
const hiddenElement = document.querySelector('input[name=option]');

if (fields[0]) {
    fields[0].removeAttribute("required");
}

window.onload = function () {
    if (hiddenElement.value === 'yes') {
        container.style.display = "block";
        fields.forEach((field) => {
            field.setAttribute("required", "");
        });
        changePasswordButton.textContent = 'Cancel';
    }
}

changePasswordButton.addEventListener("click", () => {
    if (container.style.display === "block") {
        hiddenElement.value = "no";
        container.style.display = "none";
        fields.forEach((field) => {
            field.removeAttribute("required");
            field.value = "";
        });
        changePasswordButton.textContent = 'Change password';
    } else {
        hiddenElement.value = "yes";
        container.style.display = "block";
        fields.forEach((field) => {
            field.setAttribute("required", "");
        });
        changePasswordButton.textContent = 'Cancel';
    }
});