(function () {
    const API_URL    = "/api/chat";
    const messagesEl = document.getElementById("messages");
    const input      = document.getElementById("message-input");
    const sendBtn    = document.getElementById("send-btn");
    const statusEl   = document.getElementById("chat-status");
    const suggestions= document.getElementById("suggestions");
    const welcomeEl  = document.getElementById("chat-welcome");

    if (!messagesEl || !input || !sendBtn || !statusEl) return;

    function scrollToBottom() {
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    function setStatus(text, isError) {
        statusEl.textContent = text || "";
        statusEl.classList.toggle("chat-error", Boolean(isError));
    }

    function addMessage(role, text) {
        // Esconde o painel de boas-vindas ao primeira mensagem
        if (welcomeEl) welcomeEl.style.display = 'none';

        const wrapper = document.createElement("div");
        wrapper.className = "message " + role;

        const avatar = document.createElement("div");
        avatar.className = "msg-avatar";
        avatar.textContent = role === "bot" ? "✦" : "U";

        const bubble = document.createElement("div");
        bubble.className = "msg-bubble";
        bubble.textContent = text;

        wrapper.appendChild(avatar);
        wrapper.appendChild(bubble);
        messagesEl.appendChild(wrapper);
        scrollToBottom();
    }

    async function sendMessage() {
        const content = input.value.trim();
        if (!content) return;

        addMessage("user", content);
        input.value = "";
        setStatus("Aisha está pensando...");
        sendBtn.disabled = true;
        input.disabled   = true;

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: content })
            });

            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                throw new Error(data.response || data.error || "Erro HTTP " + response.status);
            }

            addMessage("bot", data.response || "Sem resposta da IA.");
            setStatus("", false);

        } catch (error) {
            addMessage("bot", "Não consegui responder agora. Tente novamente.");
            setStatus("Erro: " + (error instanceof Error ? error.message : "Falha ao chamar a IA."), true);
        } finally {
            sendBtn.disabled = false;
            input.disabled   = false;
            input.focus();
        }
    }

    sendBtn.addEventListener("click", sendMessage);

    input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });

    // Sugestões da sidebar
    if (suggestions) {
        suggestions.addEventListener("click", function (e) {
            const target = e.target;
            if (!(target instanceof HTMLButtonElement)) return;
            input.value = target.textContent || "";
            input.focus();
            // Fecha sidebar no mobile após clicar na sugestão
            if (window.innerWidth <= 768) {
                const sidebar = document.getElementById('sidebar');
                const overlay = document.getElementById('overlay');
                sidebar && sidebar.classList.remove('open');
                overlay && overlay.classList.remove('open');
                document.body.style.overflow = '';
            }
        });
    }
})();