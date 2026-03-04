// College Chatbot - AI Powered
const API_BASE_URL = "http://localhost:5000";

function getSavedChat(){
  try{ return JSON.parse(sessionStorage.getItem('chat_history') || '[]') }catch(e){ return [] }
}

function saveChatHistory(arr){
  try{ sessionStorage.setItem('chat_history', JSON.stringify(arr)) }catch(e){}
}

function appendToSavedChat(sender, text, cls){
  if(cls === 'bot-loading') return; // don't persist loading
  const arr = getSavedChat();
  arr.push({sender, text, cls});
  saveChatHistory(arr);
}

function restoreChat(){
  const arr = getSavedChat();
  const box = document.getElementById('chatbox');
  box.innerHTML = '';
  if(arr.length === 0){
    box.innerHTML = '<div class="bot"><b>Bot:</b> Hello! I\'m an AI-powered college assistant. Ask me anything about admissions, courses, timings, hostel, placements, and more!</div>';
    return;
  }
  arr.forEach(m => {
    const msgDiv = document.createElement('div');
    msgDiv.className = m.cls;
    msgDiv.innerHTML = `<b>${m.sender}:</b> ${m.text}`;
    box.appendChild(msgDiv);
  });
  box.scrollTop = box.scrollHeight;
}

function handleKeyPress(event) {
  if(event.key === "Enter") {
    sendMessage();
  }
}

function sendMessage() {
  let input = document.getElementById("userInput");
  let msg = input.value;

  if(msg.trim() === "") return;

  addMessage("You", msg, "user");
  input.value = "";
  
  // Show loading indicator
  addMessage("Bot", "Thinking...", "bot-loading");

  fetch(API_BASE_URL + "/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: msg})
  })
  .then(res => res.json())
  .then(data => {
    // Remove loading message
    let box = document.getElementById("chatbox");
    let loadingMsg = box.querySelector(".bot-loading");
    if(loadingMsg) loadingMsg.remove();
    // If backend requests showing the first five questions, handle that
    if(data.action === "show_first_five" && Array.isArray(data.first_five)) {
      addMessage("Bot", data.reply || "Here are some suggestions:", "bot");
      displayRelatedQuestions(data.first_five);
      return;
    }

    addMessage("Bot", data.reply, "bot");

    // Display related questions if available
    if(data.related_questions && data.related_questions.length > 0) {
      displayRelatedQuestions(data.related_questions);
    }
  })
  .catch(err => {
    console.error("Error:", err);
    let box = document.getElementById("chatbox");
    let loadingMsg = box.querySelector(".bot-loading");
    if(loadingMsg) loadingMsg.remove();
    addMessage("Bot", "Sorry, I encountered an error. Please try again.", "bot-error");
  });
}

function addMessage(sender, text, cls) {
  let box = document.getElementById("chatbox");
  let msgDiv = document.createElement("div");
  msgDiv.className = cls;
  msgDiv.innerHTML = `<b>${sender}:</b> ${text}`;
  box.appendChild(msgDiv);
  box.scrollTop = box.scrollHeight;
  // persist into session until tab closed
  appendToSavedChat(sender, text, cls);
}

function displayRelatedQuestions(questions) {
  let box = document.getElementById("chatbox");
  let container = document.createElement("div");
  container.className = "related-questions";
  
  let title = document.createElement("p");
  title.className = "related-title";
  title.innerHTML = "💡 <b>Here are some related topics:</b>";
  container.appendChild(title);
  
  questions.forEach(question => {
    let btn = document.createElement("button");
    btn.className = "related-btn";
    btn.textContent = "• " + question;
    btn.onclick = () => handleRelatedQuestion(question);
    container.appendChild(btn);
  });
  
  box.appendChild(container);
  box.scrollTop = box.scrollHeight;
}

function handleRelatedQuestion(question) {
  addMessage("You", question, "user");
  addMessage("Bot", "Thinking...", "bot-loading");
  
  fetch(API_BASE_URL + "/get-answer", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question: question})
  })
  .then(res => res.json())
  .then(data => {
    let box = document.getElementById("chatbox");
    let loadingMsg = box.querySelector(".bot-loading");
    if(loadingMsg) loadingMsg.remove();
    
    if(data.success) {
      addMessage("Bot", data.answer, "bot");
    } else {
      addMessage("Bot", data.error || "Answer not found.", "bot-error");
    }
  })
  .catch(err => {
    console.error("Error:", err);
    let box = document.getElementById("chatbox");
    let loadingMsg = box.querySelector(".bot-loading");
    if(loadingMsg) loadingMsg.remove();
    addMessage("Bot", "Error fetching answer.", "bot-error");
  });
}

// restore chat on load
document.addEventListener('DOMContentLoaded', () => {
  try{ restoreChat(); }catch(e){}
});