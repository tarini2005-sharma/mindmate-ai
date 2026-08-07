// ===============================
// MindMate Intake Page
// Temporary Frontend Logic
// Backend integration later
// ===============================

document.addEventListener("DOMContentLoaded", () => {

    // ===============================
    // CHIP BUTTONS (Multiple Selection)
    // ===============================

    const chips = document.querySelectorAll(".chip");

    chips.forEach(chip => {

        chip.addEventListener("click", () => {

            chip.classList.toggle("active");

        });

    });



    // ===============================
    // RATING BUTTONS (Single Selection)
    // ===============================

    const ratingButtons = document.querySelectorAll(".rating-btn");

    ratingButtons.forEach(button => {

        button.addEventListener("click", () => {

            ratingButtons.forEach(btn =>

                btn.classList.remove("active")

            );

            button.classList.add("active");

        });

    });



    // ===============================
    // TOGGLE BUTTON GROUPS
    // (Single Selection per Group)
    // ===============================

    const toggleGroups = document.querySelectorAll(".toggle-group");

    toggleGroups.forEach(group => {

        const buttons = group.querySelectorAll(".toggle-btn");

        buttons.forEach(button => {

            button.addEventListener("click", () => {

                buttons.forEach(btn =>

                    btn.classList.remove("active")

                );

                button.classList.add("active");

            });

        });

    });

       // ==========================================
// Shared: Save Profile & Continue
// ==========================================

function saveProfileAndContinue() {

     // ---- SAFETY CHECK FIRST ----
    const safetyGroup = document.querySelectorAll(".toggle-group")[3];
    const safetyAnswer = safetyGroup
        ? safetyGroup.querySelector(".toggle-btn.active")
        : null;

    if (safetyAnswer && safetyAnswer.innerText.trim() === "Yes") {

        alert(
            "You deserve immediate support.\n\n" +
            "Please reach out to a trusted person near you, or contact a local " +
            "emergency or crisis support service right now.\n\n" +
            "If you are in immediate danger, contact your local emergency services immediately."
        );

        return;
    }


    const userId = localStorage.getItem("mindmate_user_id");

    const selectedChips = [];
    document.querySelectorAll(".chip.active").forEach(chip => {
        selectedChips.push(chip.innerText);
    });

    const toggleAnswers = [];
    document.querySelectorAll(".toggle-group").forEach(group => {
        const active = group.querySelector(".toggle-btn.active");
        toggleAnswers.push(active ? active.innerText : "");
    });

    const coping = document.getElementById("coping").value;

    const profilePayload = {
        user_id: userId,
        occupation: null,
        common_emotions: selectedChips,
        common_triggers: [],
        helpful_activities: coping
            ? coping.split(",").map(item => item.trim()).filter(Boolean)
            : [],
        unhelpful_activities: [],
        preferred_support_style: toggleAnswers[0] || null
    };

    fetch("http://127.0.0.1:8000/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(profilePayload)
    })
    .then(res => res.json())
    .then(data => {
        console.log("Profile saved:", data);
        window.location.href = "dashboard.html";
    })
    .catch(err => {
        console.error("Failed to save profile:", err);
        window.location.href = "dashboard.html";
    });
}


// ==========================================
// Skip Button
// ==========================================

const skipBtn = document.getElementById("skipBtn");

if (skipBtn) {
    skipBtn.addEventListener("click", () => {
        saveProfileAndContinue();
    });
}


// ==========================================
// Continue Button
// ==========================================

const intakeForm = document.getElementById("intakeForm");

intakeForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const consent = document.getElementById("consent");
    if (!consent.checked) {
        alert("Please accept the consent before continuing.");
        return;
    }

    saveProfileAndContinue();
});
});