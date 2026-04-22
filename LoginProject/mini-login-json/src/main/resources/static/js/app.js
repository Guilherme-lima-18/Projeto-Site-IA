(function () {
    // ── Hamburger / Sidebar mobile ──────────────────────────
    const hamburger = document.getElementById('hamburger');
    const sidebar   = document.getElementById('sidebar');
    const overlay   = document.getElementById('overlay');

    function openSidebar() {
        sidebar  && sidebar.classList.add('open');
        overlay  && overlay.classList.add('open');
        document.body.style.overflow = 'hidden';
    }

    function closeSidebar() {
        sidebar  && sidebar.classList.remove('open');
        overlay  && overlay.classList.remove('open');
        document.body.style.overflow = '';
    }

    hamburger && hamburger.addEventListener('click', openSidebar);
    overlay   && overlay.addEventListener('click', closeSidebar);

    // Fecha sidebar ao redimensionar para desktop
    window.addEventListener('resize', function () {
        if (window.innerWidth > 768) closeSidebar();
    });

    // ── Avatar: inicial do nome do usuário ──────────────────
    const avatarEl = document.getElementById('user-avatar-initial');
    if (avatarEl) {
        const nameEl = document.querySelector('.user-name');
        if (nameEl && nameEl.textContent.trim()) {
            avatarEl.textContent = nameEl.textContent.trim().charAt(0).toUpperCase();
        }
    }

    // ── Botão Novo Chat ─────────────────────────────────────
    const btnNewChat = document.getElementById('btn-new-chat');
    if (btnNewChat) {
        btnNewChat.addEventListener('click', function (e) {
            e.preventDefault();
            const messagesEl = document.getElementById('messages');
            const welcomeEl  = document.getElementById('chat-welcome');
            const statusEl   = document.getElementById('chat-status');

            if (messagesEl) {
                // Remove todas as mensagens exceto o welcome
                Array.from(messagesEl.children).forEach(function (child) {
                    if (child.id !== 'chat-welcome') child.remove();
                });

                // Mostra boas-vindas de novo
                if (welcomeEl) welcomeEl.style.display = '';

                // Adiciona mensagem inicial da Aisha
                const bubble = document.createElement('div');
                bubble.className = 'message bot';
                bubble.innerHTML = '<div class="msg-avatar">✦</div><div class="msg-bubble">Chat reiniciado! Como posso te ajudar?</div>';
                messagesEl.appendChild(bubble);
            }

            if (statusEl) statusEl.textContent = '';

            // Foca no input
            const input = document.getElementById('message-input');
            input && input.focus();

            // Fecha sidebar no mobile
            if (window.innerWidth <= 768) closeSidebar();
        });
    }
})();