document.addEventListener("DOMContentLoaded", () => {

    const userInput = document.getElementById("user-input");
    const chatContainer = document.querySelector(".chat-container");
    const sendBtn = document.querySelector(".send-btn");

    // Agregar mensajes al chat
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

    // Enviar pregunta al backend REAL
    async function sendQuestion() {
        const question = userInput.value.trim();
        if (!question) return;

        addMessage(question, "user");
        userInput.value = "";

        // Mensaje temporal
        addMessage("Thinking...", "bot");

        try {
            const response = await fetch("http://127.0.0.1:8000/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ question: question })
            });

            const data = await response.json();

            const lastBotMessage = chatContainer.querySelector(".message.bot:last-child .message-text");

            if (data.answer) {
                lastBotMessage.textContent = data.answer;
            } else {
                lastBotMessage.textContent = "No response received from server.";
            }

        } catch (error) {
            const lastBotMessage = chatContainer.querySelector(".message.bot:last-child .message-text");
            lastBotMessage.textContent = "Error connecting to backend.";
            console.error(error);
        }
    }

    // Eventos
    sendBtn.addEventListener("click", sendQuestion);

    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendQuestion();
        }
    });

});