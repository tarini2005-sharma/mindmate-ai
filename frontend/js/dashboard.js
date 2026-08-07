/* ==========================================
   MINDMATE DASHBOARD
   PART 1
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* ==============================
       SELECT ELEMENTS
    ============================== */

    const moodChips = document.querySelectorAll(".mood-chip");

    const form = document.getElementById("analyzeForm");

    const input = document.getElementById("emotionInput");

    const analyzeBtn = document.getElementById("analyzeBtn");

    const userMessage = document.getElementById("userMessage");

    const aiMessage = document.getElementById("messageResult");

    const emotionResult = document.getElementById("emotionResult");

    const anxietyScore = document.getElementById("anxietyScore");

    

    const intensityResult = document.getElementById("intensityResult");


    /* ==============================
   LOAD REAL HISTORY + SUMMARY
============================== */

const userId = localStorage.getItem("mindmate_user_id");

if (userId) {
    fetch(`http://127.0.0.1:8000/mood-history/${userId}`)
        .then(res => res.json())
        .then(data => renderHistory(data.history))
        .catch(err => console.error("Failed to load history:", err));

    fetch(`http://127.0.0.1:8000/mood-summary/${userId}`)
        .then(res => res.json())
        .then(data => renderSummary(data.summary))
        .catch(err => console.error("Failed to load summary:", err));
}

function renderHistory(history) {
    const container = document.getElementById("historyContainer");
    container.innerHTML = "";

    if (history.length === 0) {
        container.innerHTML = `<div class="history-item"><span class="history-day">No entries yet</span></div>`;
        return;
    }

    history.slice(0, 6).forEach(entry => {
        const date = new Date(entry.created_at);
        const dayLabel = date.toLocaleDateString(undefined, { weekday: "short" });

        const item = document.createElement("div");
        item.className = "history-item";
        item.innerHTML = `
            <span class="history-day">${dayLabel}</span>
            <span class="history-tag">${entry.emotion.replace("_", " ")}</span>
        `;
        container.appendChild(item);
    });
}

function renderSummary(summary) {
    const panelTitle = document.querySelector(".insight-divider").previousElementSibling;
    // Replace right-panel insight items with real emotion breakdown
    const insightItems = document.querySelectorAll(".insight-item");
    insightItems.forEach(item => item.remove());

    const insertBefore = document.querySelector(".insight-divider");
    const container = insertBefore.parentElement;

    if (!summary.emotion_breakdown || summary.emotion_breakdown.length === 0) {
        const empty = document.createElement("p");
        empty.textContent = "No check-ins yet this week.";
        empty.style.color = "var(--text-muted)";
        empty.style.fontSize = "13px";
        container.insertBefore(empty, insertBefore);
        return;
    }

    const maxCount = Math.max(...summary.emotion_breakdown.map(e => e.count));

    summary.emotion_breakdown.forEach(entry => {
        const pct = Math.round((entry.count / maxCount) * 100);

        const el = document.createElement("div");
        el.className = "insight-item";
        el.innerHTML = `
            <div class="insight-top">
                <span class="insight-name">${entry.emotion.replace("_", " ")}</span>
                <span class="insight-score">${entry.count}</span>
            </div>
            <div class="bar-track">
                <div class="bar-fill" style="width:${pct}%;"></div>
            </div>
        `;
        container.insertBefore(el, insertBefore);
    });

    document.getElementById("recommendationReason").innerHTML =
        `This week: <b>${summary.total_checkins}</b> check-ins, most common feeling was <b>${summary.most_common_emotion?.replace("_", " ") || "n/a"}</b>.`;
}



    /* ==============================
       MOOD CHIP SELECTION
    ============================== */

    moodChips.forEach(chip => {

        chip.addEventListener("click", () => {

            moodChips.forEach(c => c.classList.remove("active"));

            chip.classList.add("active");

        });

    });



    /* ==============================
       ANALYZE FORM
    ============================== */

    form.addEventListener("submit", function (e) {

        e.preventDefault();

        const text = input.value.trim();

        if (text === "") return;



        /* USER MESSAGE */

        userMessage.textContent = text;



        /* LOADING STATE */

        analyzeBtn.disabled = true;

        analyzeBtn.textContent = "...";



        aiMessage.textContent =

            "Analyzing your emotions...";



        emotionResult.textContent = "--";

        anxietyScore.textContent = "--";

        

        intensityResult.textContent = "--";



        /* REAL API CALL */

const userId = localStorage.getItem("mindmate_user_id");

fetch("http://127.0.0.1:8000/personalized-analyze", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        user_id: userId,
        text: text
    })
})
.then(res => res.json())
.then(data => {


    // ---- SAFETY SHORT-CIRCUIT ----
    if (data.safety && data.safety.risk_detected) {

        aiMessage.textContent = data.message;

        emotionResult.textContent = "--";
        anxietyScore.textContent = "--";
        
        intensityResult.textContent = "--";

        // Simple crisis emphasis — swap bubble styling
        aiMessage.parentElement.style.border = "1px solid var(--coral)";
        aiMessage.parentElement.style.background = "rgba(232,115,122,.12)";

        return;
    }

    // ---- NORMAL RESULT ----
    const analysis = data.analysis;

    emotionResult.textContent = analysis.emotion;
    intensityResult.textContent = analysis.confidence > 0.7 ? "High" : "Medium";

    // Your model only returns one emotion + confidence,
    // not separate anxiety/stress/loneliness scores —
    // so we just show confidence in the anxiety slot for now
    anxietyScore.textContent = analysis.confidence.toFixed(2);
    

    aiMessage.textContent =
        `It sounds like you may be feeling ${analysis.emotion.replace("_", " ")}.`;

    // Update the recommendation card with the top activity
    if (analysis.activities && analysis.activities.length > 0) {
        const top = analysis.activities[0];
        activityTitle.textContent = top.activity;
        activityReason.textContent = top.reason;
    }

    renderHistory ? fetch(`http://127.0.0.1:8000/mood-history/${userId}`).then(r=>r.json()).then(d=>renderHistory(d.history)) : null;
fetch(`http://127.0.0.1:8000/mood-summary/${userId}`).then(r=>r.json()).then(d=>renderSummary(d.summary));
})
.catch(err => {
    console.error("Analyze request failed:", err);
    aiMessage.textContent = "Something went wrong reaching MindMate. Please try again.";
})
.finally(() => {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "→";
    input.value = "";
});

    });



    

    
});
/* ==========================================
   PART 2
   RECOMMENDATIONS & FEEDBACK
========================================== */

const activityTitle = document.getElementById("activityTitle");
const activityReason = document.getElementById("activityReason");

const startExerciseBtn = document.getElementById("startExerciseBtn");
const anotherOptionBtn = document.getElementById("anotherOptionBtn");
const feedbackBtn = document.getElementById("feedbackBtn");


/* ==========================================
   RECOMMENDED ACTIVITIES
========================================== */

const activities = [

    {

        title: "5-4-3-2-1 Grounding Exercise",

        reason:
        "Grounding has helped you the most during high anxiety in previous sessions."

    },

    {

        title: "Deep Breathing",

        reason:
        "Slow breathing helps reduce physical symptoms of stress."

    },

    {

        title: "Take a Short Walk",

        reason:
        "A brief walk can improve mood and reduce anxious thoughts."

    },

    {

        title: "Listen to Relaxing Music",

        reason:
        "Music may help calm your mind and lower stress."

    },

    {

        title: "Write Your Thoughts",

        reason:
        "Journaling helps organize racing thoughts."

    }

];

let currentActivity = 0;


/* ==========================================
   SHOW ANOTHER OPTION
========================================== */

anotherOptionBtn.addEventListener("click", () => {

    currentActivity++;

    if (currentActivity >= activities.length) {

        currentActivity = 0;

    }

    activityTitle.style.opacity = "0";

    activityReason.style.opacity = "0";

    setTimeout(() => {

        activityTitle.textContent =
            activities[currentActivity].title;

        activityReason.textContent =
            activities[currentActivity].reason;

        activityTitle.style.opacity = "1";

        activityReason.style.opacity = "1";

    }, 200);

});


/* ==========================================
   START EXERCISE
========================================== */

startExerciseBtn.addEventListener("click", () => {

    startExerciseBtn.textContent = "Starting...";

    startExerciseBtn.disabled = true;

    setTimeout(() => {

        alert(

            "Exercise Mode\n\n" +

            "Take a slow deep breath.\n\n" +

            "Now notice:\n\n" +

            "5 things you can SEE\n" +

            "4 things you can TOUCH\n" +

            "3 things you can HEAR\n" +

            "2 things you can SMELL\n" +

            "1 thing you can TASTE"

        );

        startExerciseBtn.textContent = "Exercise Started ✓";

    }, 700);

});


/* ==========================================
   FEEDBACK BUTTON
========================================== */

feedbackBtn.addEventListener("click", () => {

    feedbackBtn.textContent = "✓ Thank you!";

    feedbackBtn.style.background = "var(--sage)";

    feedbackBtn.style.color = "#10201A";

    feedbackBtn.style.fontWeight = "600";

    feedbackBtn.disabled = true;

});


/* ==========================================
   SMOOTH TRANSITIONS
========================================== */

activityTitle.style.transition = "0.25s";

activityReason.style.transition = "0.25s";

feedbackBtn.style.transition = "0.25s";

startExerciseBtn.style.transition = "0.25s";

anotherOptionBtn.style.transition = "0.25s";
/* ==========================================
   PART 3
   READY FOR BACKEND INTEGRATION
========================================== */

/*
    This function will later call

    POST /analyze

    Currently it simply updates all UI elements.

    Later replace the body of this function with fetch().
*/

function updateDashboard(data){

    /* ---------- Chat Response ---------- */

    messageResult.textContent = data.message;

    /* ---------- Emotion Pills ---------- */

    emotionResult.textContent = data.emotion;

    anxietyScore.textContent = data.anxiety;

   
    intensityResult.textContent = data.intensity;

    /* ---------- Recommendation ---------- */

    activityTitle.textContent = data.activity;

    activityReason.textContent = data.reason;

}


/* ==========================================
   SAMPLE DATA
========================================== */

const sampleResponses = [

{

emotion:"Anxiety",

anxiety:"0.88",

stress:"0.71",

loneliness:"0.22",

intensity:"High",

activity:"5-4-3-2-1 Grounding Exercise",

reason:"Grounding has worked best during previous anxiety check-ins.",

message:
"It sounds like anxiety may be affecting you today. Try focusing on the present moment rather than worrying about future events."

},

{

emotion:"Stress",

anxiety:"0.45",

stress:"0.84",

loneliness:"0.31",

intensity:"Medium",

activity:"Deep Breathing",

reason:"Breathing exercises reduce stress and improve relaxation.",

message:
"It seems you're experiencing stress. Taking a few slow breaths may help calm your nervous system."

},

{

emotion:"Loneliness",

anxiety:"0.22",

stress:"0.41",

loneliness:"0.93",

intensity:"High",

activity:"Reach out to Someone",

reason:"Talking with someone you trust often helps reduce loneliness.",

message:
"It sounds like loneliness may be affecting you. Consider connecting with someone you trust."

}

];


/* ==========================================
   RANDOM DEMO
========================================== */

function randomDemo(){

    const random=

    sampleResponses[

        Math.floor(

            Math.random()*sampleResponses.length

        )

    ];

    updateDashboard(random);

}


/* ==========================================
   DEMO MODE
========================================== */

/*

    Double-click logo

    ↓

    Loads random prediction

*/

const logo=document.querySelector(".brand-mark");

if(logo){

logo.addEventListener("dblclick",()=>{

randomDemo();

});

}


/* ==========================================
   FUTURE BACKEND
========================================== */

/*

Replace

fakeAnalysis(text)

with

fetch("http://127.0.0.1:8000/analyze",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

user_id:"user123",

text:text

})

})

.then(res=>res.json())

.then(data=>{

updateDashboard({

emotion:data.emotion,

anxiety:data.confidence.anxiety,

stress:data.confidence.stress,

loneliness:data.confidence.loneliness,

intensity:data.intensity,

activity:data.activity,

reason:data.reason,

message:data.message

});

});

*/

/* ==========================================
   END
========================================== */

console.log("MindMate Dashboard Ready 🚀");