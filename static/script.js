document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("chat-form");
  const questionInput = document.getElementById("question");
  const chatBox = document.getElementById("chat-box");
  const chatLinks = document.querySelectorAll(".chat-link");
  const newChatBtn = document.querySelector(".new-chat-btn");

  const SESSION_CHAT_KEY = "sessionChat";
  const ACTIVE_CHAT_ID_KEY = "activeChatId";

  // Load chat from sessionStorage or fetch from DB
  function loadChat(chatId = null) {
    const activeChatId = chatId || sessionStorage.getItem(ACTIVE_CHAT_ID_KEY);
    if (activeChatId) {
      // Fetch specific chat history from the backend
      fetch(`/history/${activeChatId}`)
        .then(res => res.json())
        .then(data => {
          chatBox.innerHTML = "";
          if (data.chat) {
            addMessage("user", data.chat.question);
            addMessage("bot", data.chat.response);
          }
          sessionStorage.setItem(ACTIVE_CHAT_ID_KEY, activeChatId);
        });
    } else {
      // Load current session chat if no active chat is selected
      const sessionChat = JSON.parse(sessionStorage.getItem(SESSION_CHAT_KEY) || "[]");
      chatBox.innerHTML = "";
      sessionChat.forEach(msg => addMessage(msg.role, msg.text));
    }
  }

  // Save message to current session
  function saveMessageToSession(role, text) {
    const sessionChat = JSON.parse(sessionStorage.getItem(SESSION_CHAT_KEY) || "[]");
    sessionChat.push({ role, text });
    sessionStorage.setItem(SESSION_CHAT_KEY, JSON.stringify(sessionChat));
  }

  // Event listener for chat history links
  chatLinks.forEach(link => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const chatId = this.dataset.chatId;
      sessionStorage.removeItem(SESSION_CHAT_KEY); // Clear session chat
      loadChat(chatId);
    });
  });

  // Event listener for the New Chat button
  newChatBtn.addEventListener("click", function (e) {
    e.preventDefault();
    sessionStorage.removeItem(ACTIVE_CHAT_ID_KEY);
    sessionStorage.removeItem(SESSION_CHAT_KEY);
    window.location.href = "/"; // Redirect to home for a fresh start
  });

  // Initial load
  loadChat();

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const question = questionInput.value.trim();
    if (!question) return;

    // If starting a new chat, clear the active chat ID
    const activeChatId = sessionStorage.getItem(ACTIVE_CHAT_ID_KEY);
    if (activeChatId) {
      sessionStorage.removeItem(ACTIVE_CHAT_ID_KEY);
      chatBox.innerHTML = '';
    }

    addMessage("user", question);
    saveMessageToSession("user", question);
    questionInput.value = "";

    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();
    const reply = data.response || data.error || "No response";
    addMessage("bot", reply);
    saveMessageToSession("bot", reply);
  });

  function addMessage(role, text) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", role);
    msgDiv.textContent = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
  }
});
