(function () {
    const API_URL = "/api/chat";
    const messages = document.getElementById("messages");
    const input = document.getElementById("message-input");
    const sendBtn = document.getElementById("send-btn");
    const status = document.getElementById("chat-status");
    const suggestions = document.getElementById("suggestions");

    if (!messages || !input || !sendBtn || !status) {
        return;
    }

    function scrollToBottom() {
        messages.scrollTop = messages.scrollHeight;
    }

    function setStatus(text, isError) {
        status.textContent = text || "";
        status.classList.toggle("chat-error", Boolean(isError));
    }

    function addMessage(role, text) {
        const bubble = document.createElement("div");
        bubble.className = `message ${role}`;
        bubble.textContent = text;
        messages.appendChild(bubble);
        scrollToBottom();
    }

    async function sendMessage() {
        const content = input.value.trim();
        if (!content) {
            return;
        }

        addMessage("user", content);
        input.value = "";
        setStatus("Aisha está pensando...");
        sendBtn.disabled = true;
        input.disabled = true;

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: content })
            });

            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                const apiError = data.response || data.error || `Erro HTTP ${response.status}`;
                throw new Error(apiError);
            }

            addMessage("bot", data.response || "Sem resposta da IA.");
            setStatus("", false);
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : "Falha ao chamar a IA.";
            addMessage("bot", "Não consegui responder agora. Tente novamente.");
            setStatus(`Erro: ${errorMessage}`, true);
        } finally {
            sendBtn.disabled = false;
            input.disabled = false;
            input.focus();
        }
    }

    sendBtn.addEventListener("click", sendMessage);

    input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });

    if (suggestions) {
        suggestions.addEventListener("click", function (event) {
            const target = event.target;
            if (!(target instanceof HTMLButtonElement)) {
                return;
            }

            input.value = target.textContent || "";
            input.focus();
        });
    }
})();