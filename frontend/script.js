document.addEventListener("DOMContentLoaded", () => {

    const userInput = document.getElementById("user-input");
    const chatContainer = document.querySelector(".chat-container");
    const sendBtn = document.querySelector(".send-btn");

    let isLoading = false;

    function scrollToBottom() {
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: "smooth"
        });
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

    // =========================
    // SOURCES (FIX COMPATIBLE)
    // =========================
    function addSources(sources, parentMessage) {

        if (!parentMessage) return;
        if (!sources || !Array.isArray(sources) || sources.length === 0) return;

        const contentDiv = parentMessage.querySelector(".message-content");

        if (contentDiv.querySelector(".sources-box")) return;

        const toggleBtn = document.createElement("div");
        toggleBtn.classList.add("sources-toggle");
        toggleBtn.textContent = "Ver fuentes";

        const sourcesBox = document.createElement("div");
        sourcesBox.classList.add("sources-box");

        sources.forEach(src => {

            const item = document.createElement("div");
            item.classList.add("source-item");

            const name =
                src.source ||
                src.doc_id ||
                src.chunk_uid ||
                "unknown source";

            const chunkInfo =
                src.chunk_id !== undefined && src.chunk_id !== null
                    ? ` | chunk: ${src.chunk_id}`
                    : "";

            item.textContent = `${name}${chunkInfo}`.trim();

            sourcesBox.appendChild(item);
        });

        toggleBtn.addEventListener("click", () => {
            const isOpen = sourcesBox.classList.toggle("open");
            toggleBtn.textContent = isOpen ? "Ocultar fuentes" : "Ver fuentes";
        });

        contentDiv.appendChild(toggleBtn);
        contentDiv.appendChild(sourcesBox);

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
                headers: {
                    "Content-Type": "application/json"
                },
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
                    requestAnimationFrame(() => {
                        setTimeout(typeWriter, 10);
                    });
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