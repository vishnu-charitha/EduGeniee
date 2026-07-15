// ==========================================================
// EduGenie Dashboard Controller
// ==========================================================

const promptBox = document.getElementById("prompt");
const responseBox = document.getElementById("chatArea");
const taskSelect = document.getElementById("task");
const statusText = document.getElementById("status");

const generateBtn = document.getElementById("generateBtn");
const copyBtn = document.getElementById("copyBtn");
const clearBtn = document.getElementById("clearBtn");
const token = localStorage.getItem("token");

if(!token){

    window.location.href="/login";

}
// ==========================================================
// Initialize
// ==========================================================

window.onload = () => {

    initialize();

    loadProfile();

    loadStats();

    loadHistory();

};
async function loadProfile(){

    const token = localStorage.getItem("token");

    const response = await fetch("/auth/me",{

        headers:{

            "Authorization":`Bearer ${token}`

        }

    });

    if(response.ok){

        const user = await response.json();

        const nameElement = document.getElementById("username");

        if(nameElement){

            nameElement.innerHTML = user.name;

        }

    }

}
function renderQuiz(quiz){

    let html = "";

    quiz.forEach((q,index)=>{

        // Convert A/B/C/D into actual answer text
        let correctAnswer = "";

        switch(q.correct_answer){

            case "A":
                correctAnswer = q.option_a;
                break;

            case "B":
                correctAnswer = q.option_b;
                break;

            case "C":
                correctAnswer = q.option_c;
                break;

            case "D":
                correctAnswer = q.option_d;
                break;

            default:
                correctAnswer = q.correct_answer;
        }

        const explanation = q.explanation || "No explanation available.";

        html += `

        <div class="quiz-card">

            <h2>Question ${index+1}</h2>

            <p class="quiz-question">

                ${q.question}

            </p>

            <div class="options">

                <label class="option-card">

                    <input
                        type="radio"
                        name="q${index}"
                        value="${q.option_a}">

                    <span>${q.option_a}</span>

                </label>

                <label class="option-card">

                    <input
                        type="radio"
                        name="q${index}"
                        value="${q.option_b}">

                    <span>${q.option_b}</span>

                </label>

                <label class="option-card">

                    <input
                        type="radio"
                        name="q${index}"
                        value="${q.option_c}">

                    <span>${q.option_c}</span>

                </label>

                <label class="option-card">

                    <input
                        type="radio"
                        name="q${index}"
                        value="${q.option_d}">

                    <span>${q.option_d}</span>

                </label>

            </div>

            <button
                class="submit-answer"
                onclick="checkAnswer(
                    ${index},
                    '${correctAnswer.replace(/'/g, "\\'")}',
                    '${explanation.replace(/'/g, "\\'")}'
                )">

                Submit Answer

            </button>

            <div
                id="result${index}"
                class="quiz-result">

            </div>

        </div>

        `;

    });

    responseBox.innerHTML = html;

}

function checkAnswer(index, correctAnswer, explanation){

    const selected = document.querySelector(
        `input[name="q${index}"]:checked`
    );

    const result =
    document.getElementById(`result${index}`);

    if(!selected){

        result.innerHTML = `

        <div class="warning">

            Please select an option.

        </div>

        `;

        return;

    }

    if(selected.value === correctAnswer){

        result.innerHTML = `

        <div class="correct-answer">

            <h3>✅ Correct!</h3>

            <p>

                ${explanation}

            </p>

        </div>

        `;

    }

    else{

        result.innerHTML = `

        <div class="wrong-answer">

            <h3>❌ Incorrect</h3>

            <p>

                <strong>Your Answer:</strong>

                ${selected.value}

            </p>

            <p>

                <strong>Correct Answer:</strong>

                ${correctAnswer}

            </p>

            <hr>

            <p>

                ${explanation}

            </p>

        </div>

        `;

    }

}
function getTask() {

    const task = document.getElementById("task");

    if (!task) {
        return "question";
    }

    return task.value;

}

function initialize(){

    if(generateBtn){
    console.log("Dashboard initialized");

    generateBtn.onclick = function(){

        console.log("Generate Clicked");

        generateAI();

    };


    }

    if(copyBtn){

        copyBtn.onclick = copyResponse;

    }

    if(clearBtn){

        clearBtn.onclick = clearChat;

    }

    if(promptBox){

        promptBox.addEventListener("keydown",handleKeyboard);

        promptBox.addEventListener("input",autoResize);

    }

}

// ==========================================================
// Keyboard Shortcut
// ==========================================================

function handleKeyboard(e){

    if(e.ctrlKey && e.key==="Enter"){

        generateAI();

    }

}

// ==========================================================
// Auto Resize Textarea
// ==========================================================

function autoResize(){

    promptBox.style.height="auto";

    promptBox.style.height=promptBox.scrollHeight+"px";

}

// ==========================================================
// Copy Chat
// ==========================================================

function copyResponse(){

    navigator.clipboard.writeText(

        responseBox.innerText

    );

    showToast("Copied Successfully");

}

// ==========================================================
// Clear Chat
// ==========================================================

function clearChat(){

    responseBox.innerHTML=`

    <div class="welcome">

        <h2>

            👋 Welcome to EduGenie

        </h2>

        <p>

            Ask your first question to begin learning.

        </p>

    </div>

    `;

}

// ==========================================================
// Logout
// ==========================================================

function logout(){

    localStorage.removeItem("token");

    window.location.href="/login";

}

// ==========================================================
// Toast Message
// ==========================================================

function showToast(message){

    const toast=document.createElement("div");

    toast.className="toast show";

    toast.innerHTML=message;

    document.body.appendChild(toast);

    setTimeout(()=>{

        toast.remove();

    },2500);

}

// ==========================================================
// Loading Animation
// ==========================================================

function loading(){

    statusText.innerHTML="Generating...";

    responseBox.innerHTML+=`

    <div
        class="loading-container"
        id="loading">

        <div class="loader"></div>

        <p>

            EduGenie is Thinking...

        </p>

    </div>

    `;

    responseBox.scrollTop=responseBox.scrollHeight;

}

// ==========================================================
// User Message
// ==========================================================

function addUserMessage(text){

    responseBox.innerHTML+=`

    <div class="user-message fade-in">

        <div class="message-header">

            👤 You

        </div>

        <div class="message-body">

            ${text}

        </div>

    </div>

    `;

    responseBox.scrollTop=responseBox.scrollHeight;

}

// ==========================================================
// AI Message
// ==========================================================

function addAIMessage(){

    const div=document.createElement("div");

    div.className="ai-message fade-in";

    responseBox.appendChild(div);

    responseBox.scrollTop=responseBox.scrollHeight;

    return div;

}

// ==========================================================
// Typewriter Animation
// ==========================================================

function typeWriter(text){

    const loadingBox=document.getElementById("loading");

    if(loadingBox){

        loadingBox.remove();

    }

    const ai=addAIMessage();

    statusText.innerHTML="Writing...";

    let i=0;

    let buffer="";

    function typing(){

        if(i<text.length){

            buffer+=text.charAt(i);

            if(typeof marked!=="undefined"){

                ai.innerHTML=marked.parse(buffer);

            }

            else{

                ai.innerHTML=buffer.replace(/\n/g,"<br>");

            }

            if(window.hljs){

                document.querySelectorAll("pre code").forEach((block)=>{

                    hljs.highlightElement(block);

                });

            }

            responseBox.scrollTop=responseBox.scrollHeight;

            i++;

            setTimeout(typing,8);

        }

        else{

            statusText.innerHTML="Completed";

        }

    }

    typing();

}
function displayResult(data){

    if(data.answer){

        typeWriter(data.answer);

    }

    else if(data.explanation){

        typeWriter(data.explanation);

    }

    else if(data.summary){

        typeWriter(data.summary);

    }

    else if(data.learning_path){

        typeWriter(data.learning_path);

    }

    else if(data.quiz){

        renderQuiz(data.quiz);

    }

    else{

        typeWriter(JSON.stringify(data,null,2));

    }

}