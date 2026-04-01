document.addEventListener("DOMContentLoaded", () => {

    const userInput = document.getElementById("user-input");
    const chatContainer = document.querySelector(".chat-container");
    const sendBtn = document.querySelector(".send-btn");

    // Crear mensaje tipo bubble
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

        return messageDiv;
    }

    // Indicador typing real (bubble animada simple)
    function addTypingIndicator() {
        const typingDiv = document.createElement("div");
        typingDiv.classList.add("message", "bot", "typing");

        const avatarDiv = document.createElement("div");
        avatarDiv.classList.add("message-avatar");
        avatarDiv.textContent = "📊";

        const contentDiv = document.createElement("div");
        contentDiv.classList.add("message-content");

        const dots = document.createElement("div");
        dots.classList.add("typing-dots");
        dots.textContent = "Typing...";

        contentDiv.appendChild(dots);
        typingDiv.appendChild(avatarDiv);
        typingDiv.appendChild(contentDiv);

        chatContainer.appendChild(typingDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        return typingDiv;
    }

    // Enviar pregunta al backend
    async function sendQuestion() {
        const question = userInput.value.trim();
        if (!question) return;

        // user bubble
        addMessage(question, "user");
        userInput.value = "";

        // typing bubble
        const typingMessage = addTypingIndicator();

        try {
            const response = await fetch("http://127.0.0.1:8000/api/v1/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ question })
            });

            const data = await response.json();

            // eliminar typing
            typingMessage.remove();

            // -------------------------------
            // 🔥 TYPEWRITER EFFECT (AQUÍ EL CAMBIO)
            // -------------------------------
            const botMessage = addMessage("", "bot");
            const textElement = botMessage.querySelector(".message-text");

            const text = data.answer || "No response received";
            let i = 0;

            function typeWriter() {
                if (i < text.length) {
                    textElement.textContent += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, 15);
                }
            }

            typeWriter();

        } catch (error) {
            typingMessage.remove();
            addMessage("Error connecting to backend.", "bot");
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