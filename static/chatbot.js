function sendMessage() {

let input = document.getElementById("userInput");

let message = input.value;

if (message.trim() === "") return;

addUserMessage(message);

// 👇 إرسال الرسالة للـ AI
fetch("/ask", {

method: "POST",

headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({
message: message
})

})

.then(response => response.json())

.then(data => {

addBotMessage(data.reply);

})

.catch(error => {

addBotMessage("⚠ Error contacting AI");

console.error(error);

});

input.value = "";

}



// ================= GENERATE QUIZ =================

function generateQuiz() {

let input = document.getElementById("userInput");

let message = input.value;

// 👇 إرسال message (مهم)
fetch("/quiz", {

method: "POST",

headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({
message: message
})

})

.then(response => response.json())

.then(data => {

addBotMessage(data.quiz);

})

.catch(error => {

addBotMessage("⚠ Quiz error");

console.error(error);

});

}



// ================= SUMMARIZE =================

function summarizeChapter() {

let input = document.getElementById("userInput");

let message = input.value;

// 👇 إرسال message (ده اللي كان ناقص)
fetch("/summarize", {

method: "POST",

headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({
message: message
})

})

.then(response => response.json())

.then(data => {

addBotMessage(data.summary);

})

.catch(error => {

addBotMessage("⚠ Summary error");

console.error(error);

});

}



// ================= UI =================

function addUserMessage(message) {

let chatBox = document.getElementById("chatBox");

let msg = document.createElement("div");

msg.className = "user-message";

msg.innerText = message;

chatBox.appendChild(msg);

chatBox.scrollTop = chatBox.scrollHeight;

}



function addBotMessage(message) {

let chatBox = document.getElementById("chatBox");

let msg = document.createElement("div");

msg.className = "bot-message";

msg.innerText = message;

chatBox.appendChild(msg);

chatBox.scrollTop = chatBox.scrollHeight;

}