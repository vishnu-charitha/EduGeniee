// ==========================================================
// EduGenie API Controller
// ==========================================================



// ==========================================================
// Generate AI
// ==========================================================

async function generateAI() {

    const prompt = document.getElementById("prompt").value.trim();

    if (prompt === "") {
        showToast("Please enter a question.");
        return;
    }

    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "/login";
        return;
    }

    addUserMessage(prompt);

    loading();

    let url = "";
    let body = {};

    switch (getTask()) {

        case "question":

            url = "/ask/";
            body = {
                question: prompt
            };
            break;

        case "explanation":

            url = "/explain/";
            body = {
                topic: prompt
            };
            break;

        case "quiz":

            url = "/quiz/";
            body = {
                topic: prompt
            };
            break;

        case "summary":

            url = "/summary/";
            body = {
                text: prompt
            };
            break;

        case "learning":

            url = "/learning-path/";
            body = {
                topic: prompt
            };
            break;

        default:

            showToast("Invalid Task");
            return;
    }

    try {

        const response = await fetch(url, {

            method: "POST",

            headers: {

                "Content-Type": "application/json",

                "Authorization": `Bearer ${token}`

            },

            body: JSON.stringify(body)

        });

        if (response.status === 401) {

            localStorage.removeItem("token");

            window.location.href = "/login";

            return;

        }

        if (!response.ok) {

            const error = await response.json();

            throw new Error(error.detail || "Server Error");

        }

        const data = await response.json();

        displayResult(data);

        document.getElementById("prompt").value = "";

        loadStats();

        loadHistory();

    }

    catch (error) {

        statusText.innerHTML = "Error";

        responseBox.innerHTML += `

        <div class="ai-message fade-in">

            <h3>⚠ Error</h3>

            <p>${error.message}</p>

        </div>

        `;

        responseBox.scrollTop = responseBox.scrollHeight;

    }

}

// ==========================================================
// Dashboard Statistics
// ==========================================================

async function loadStats() {

    try {

        const token = localStorage.getItem("token");

        if (!token) return;

        const response = await fetch("/dashboard/stats", {

            headers: {

                "Authorization": `Bearer ${token}`

            }

        });

        if (response.status === 401) {

            localStorage.removeItem("token");

            window.location.href = "/login";

            return;

        }

        const data = await response.json();

        document.getElementById("questionCount").innerText = data.questions;

        document.getElementById("quizCount").innerText = data.quizzes;

        document.getElementById("summaryCount").innerText = data.summaries;

        document.getElementById("pathCount").innerText = data.learning_paths;

    }

    catch (error) {

        console.log(error);

    }

}

// ==========================================================
// History
// ==========================================================

async function loadHistory() {

    try {

        const token = localStorage.getItem("token");

        if (!token) return;

        const response = await fetch("/dashboard/history", {

            headers: {

                "Authorization": `Bearer ${token}`

            }

        });

        if (response.status === 401) {

            localStorage.removeItem("token");

            window.location.href = "/login";

            return;

        }

        const history = await response.json();

        let html = "";

        history.forEach(item => {

            html += `

<div class="history-item">

    <h4>${item.task}</h4>

    <small>${item.created_at}</small>

    <p>${item.prompt}</p>

</div>

`;

        });

        document.getElementById("history").innerHTML = html;

    }

    catch (error) {

        console.log(error);

    }

}

// ==========================================================
// Chat Messages
// ==========================================================




// ==========================================================
// Logout
// ==========================================================

