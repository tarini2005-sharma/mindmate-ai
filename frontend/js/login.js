// ============================
// MindMate Login Page JS
// ============================

// Show / Hide Password

const passwordInput = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");

togglePassword.addEventListener("click", () => {

    if (passwordInput.type === "password") {

        passwordInput.type = "text";
        togglePassword.innerHTML = "🙈";

    } else {

        passwordInput.type = "password";
        togglePassword.innerHTML = "👁";

    }

});


// ============================
// Login Form
// ============================

loginForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (email === "" || password === "") {
        alert("Please fill all the fields.");
        return;
    }

    if (!validateEmail(email)) {
        alert("Please enter a valid email address.");
        return;
    }

    // Use email as the user_id everywhere else in the app
    localStorage.setItem("mindmate_user_id", email);

    const loginBtn = document.getElementById("loginBtn");
    loginBtn.innerHTML = "Signing In...";
    loginBtn.disabled = true;

    setTimeout(() => {
        window.location.href = "intake.html";
    }, 1200);
});



// ============================
// Email Validation
// ============================

function validateEmail(email) {

    const allowedDomains = [
        "gmail.com",
        "yahoo.com",
        "redhat.com",
        "outlook.com",
        "hotmail.com"
        // add/remove domains here as needed
    ];

    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!regex.test(email)) {
        return false;
    }

    const domain = email.split("@")[1].toLowerCase();

    return allowedDomains.includes(domain);
}



// ============================
// Google Login (Demo)
// ============================

const googleBtn = document.getElementById("googleLogin");

googleBtn.addEventListener("click", () => {

    alert("Google Login Coming Soon!");

});



// ============================
// Apple Login (Demo)
// ============================

const appleBtn = document.getElementById("appleLogin");

appleBtn.addEventListener("click", () => {

    alert("Apple Login Coming Soon!");

});



// ============================
// Small Animation
// ============================

window.addEventListener("load", () => {

    document.querySelector(".login-card").classList.add("show");

    document.querySelector(".left-side").classList.add("show");

});



// ============================
// Enter Key Support
// ============================

document.addEventListener("keydown", function(e){

    if(e.key==="Enter"){

        loginForm.requestSubmit();

    }

});



// ============================
// Auto Focus
// ============================

window.onload = function(){

    document.getElementById("email").focus();

};



// ============================
// Console
// ============================

console.log("MindMate Login Loaded Successfully 🚀");