document.addEventListener("DOMContentLoaded", () => {

    const userInput = document.getElementById("user-input");
    const chatContainer = document.querySelector(".chat-container");
    const sendBtn = document.querySelector(".send-btn");

    let isLoading = false;

    function scrollToBottom() {
        window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
    }

    function setLoading(state) {
        isLoading = state;
        sendBtn.disabled = state;
        userInput.disabled = state;
        sendBtn.style.opacity = state ? "0.6" : "1";
    }

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
        textDiv.textContent = sender === "bot" ? "" : text;

        contentDiv.appendChild(textDiv);
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);

        chatContainer.appendChild(messageDiv);
        scrollToBottom();

        return messageDiv;
    }

    function addTypingIndicator() {
        const typingDiv = document.createElement("div");
        typingDiv.classList.add("message", "bot", "typing");

        const avatarDiv = document.createElement("div");
        avatarDiv.classList.add("message-avatar");
        avatarDiv.textContent = "📊";

        const contentDiv = document.createElement("div");
        contentDiv.classList.add("message-content");

        const dots = document.createElement("div");
        dots.classList.add("message-text");
        dots.textContent = "Thinking...";

        contentDiv.appendChild(dots);
        typingDiv.appendChild(avatarDiv);
        typingDiv.appendChild(contentDiv);

        chatContainer.appendChild(typingDiv);
        scrollToBottom();

        return typingDiv;
    }

    // ====================== NUEVO TOGGLE DE FUENTES ESTILO CHATGPT ======================
    function addSources(sources, parentMessage) {
        if (!sources || !Array.isArray(sources) || sources.length === 0) return;

        const contentDiv = parentMessage.querySelector(".message-content");

        // Evitar duplicados
        if (contentDiv.querySelector(".sources-toggle")) return;

        const toggleContainer = document.createElement("div");
        toggleContainer.classList.add("sources-toggle-container");

        const toggleBtn = document.createElement("button");
        toggleBtn.classList.add("sources-btn");
        toggleBtn.innerHTML = `
            <span class="sources-icon">📚</span>
            Sources <span class="sources-count">(${sources.length})</span>
            <span class="sources-arrow">▼</span>
        `;

        const sourcesList = document.createElement("div");
        sourcesList.classList.add("sources-list");

        sources.forEach(src => {
            const item = document.createElement("div");
            item.classList.add("source-item");
            item.textContent = src.source || "Documento sin título";
            sourcesList.appendChild(item);
        });

        // Toggle functionality
        toggleBtn.addEventListener("click", () => {
            const isOpen = sourcesList.classList.toggle("open");
            toggleBtn.classList.toggle("open", isOpen);
        });

        toggleContainer.appendChild(toggleBtn);
        toggleContainer.appendChild(sourcesList);
        contentDiv.appendChild(toggleContainer);

        scrollToBottom();
    }

    async function sendQuestion() {
        const question = userInput.value.trim();
        if (!question || isLoading) return;

        addMessage(question, "user");
        userInput.value = "";

        setLoading(true);

        const typingMessage = addTypingIndicator();

        try {
            const response = await fetch("http://127.0.0.1:8000/api/v1/query", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question })
            });

            const data = await response.json();

            typingMessage.remove();

            const botMessage = addMessage("", "bot");
            const textElement = botMessage.querySelector(".message-text");

            const text = data.answer || "No response received";

            let i = 0;
            function typeWriter() {
                if (i < text.length) {
                    textElement.textContent += text[i];
                    i++;
                    requestAnimationFrame(() => setTimeout(typeWriter, 8));
                } else {
                    addSources(data.sources, botMessage);
                    setLoading(false);
                }
            }
            typeWriter();

        } catch (error) {
            typingMessage.remove();
            addMessage("Error connecting to backend.", "bot");
            setLoading(false);
            console.error(error);
        }
    }

    sendBtn.addEventListener("click", sendQuestion);
    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendQuestion();
        }
    });
});