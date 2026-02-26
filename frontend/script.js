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

// Admin functions for managing training data
async function addTrainingData() {
  const question = prompt("Enter question:");
  if (!question) return;
  
  const answer = prompt("Enter answer:");
  if (!answer) return;
  
  const category = prompt("Enter category (admissions/courses/timings/hostel/placements):", "general");
  
  try {
    const response = await fetch(API_BASE_URL + "/add-training-data", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question, answer, category})
    });
    
    const data = await response.json();
    if (data.success) {
      alert("✓ Training data added successfully!");
    } else {
      alert("Error: " + data.error);
    }
  } catch (error) {
    alert("Error: " + error.message);
  }
}

async function viewTrainingData() {
  try {
    const response = await fetch(API_BASE_URL + "/get-training-data");
    const data = await response.json();
    
    let output = "TRAINING DATA:\n\n";
    output += "College Info:\n" + JSON.stringify(data.college_info, null, 2) + "\n\n";
    output += `Total Training Entries: ${data.training_data.length}\n`;
    
    data.training_data.forEach((entry, idx) => {
      output += `\n${idx + 1}. [${entry.category}]\n`;
      output += `Q: ${entry.question}\n`;
      output += `A: ${entry.answer}`;
    });
    
    console.log(output);
    alert("Training data loaded. Check console for details.\nTotal entries: " + data.training_data.length);
  } catch (error) {
    alert("Error: " + error.message);
  }
}

async function checkHealth() {
  try {
    const response = await fetch(API_BASE_URL + "/health");
    const data = await response.json();
    
    alert(`System Status: ${data.status}\nOpenAI API: ${data.openai}\nTraining Data: ${data.training_data_count} entries`);
  } catch (error) {
    alert("Error: " + error.message);
  }
}

// restore chat on load
document.addEventListener('DOMContentLoaded', () => {
  try{ restoreChat(); }catch(e){}
});