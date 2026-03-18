const userInput = document.getElementById("user-input");
const chatContainer = document.querySelector(".chat-container");
const sendBtn = document.querySelector(".send-btn");

// Función para agregar un mensaje al chat
function addMessage(text, sender = "bot") {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);

    const avatarDiv = document.createElement("div");
    avatarDiv.classList.add("message-avatar");
    avatarDiv.textContent = sender === "bot" ? "📊" : "👤";

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("message-content");

    const textDiv = document.createElement("div");
    textDiv.classList.add("message-text");
    textDiv.textContent = text;

    contentDiv.appendChild(textDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Función para enviar la pregunta (simulación)
function sendQuestion() {
    const question = userInput.value.trim();
    if (!question) return;

    addMessage(question, "user"); // mensaje del usuario
    userInput.value = "";

    // Mensaje temporal
    addMessage("Thinking...", "bot");

    // Simular respuesta después de 1 segundo
    setTimeout(() => {
        const lastBotMessage = chatContainer.querySelector(".message.bot:last-child .message-text");
        if (lastBotMessage.textContent === "Thinking...") {
            lastBotMessage.textContent = "This is a simulated answer. The ECB aims to maintain inflation around 2% target.";
        }
    }, 1000);
}

// Eventos
sendBtn.addEventListener("click", sendQuestion);
userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendQuestion();
    }
});