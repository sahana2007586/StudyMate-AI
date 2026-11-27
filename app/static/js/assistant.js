(() => {
    const layout = document.querySelector(".assistant-layout");
    const form = document.getElementById("chat-form");
    const input = document.getElementById("message-input");
    const modeSelect = document.getElementById("study-mode");
    const messagesElement = document.getElementById("messages");
    const sendButton = document.getElementById("send-button");
    const clearButton = document.getElementById("clear-chat");
    const starterPrompts = document.getElementById("starter-prompts");
    const chatUrl = layout.dataset.chatUrl;
    const conversation = [];
    let isWaiting = false;

    function escapeHtml(value) {
        return value.replace(/[&<>"']/g, (character) => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;",
        })[character]);
    }

    function formatInline(value) {
        return value
            .replace(/`([^`]+)`/g, "<code>$1</code>")
            .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    }

    function renderMarkdown(value) {
        const codeBlocks = [];
        let safeText = escapeHtml(value).replace(
            /```([a-zA-Z0-9+#.-]*)[ \t]*\n?([\s\S]*?)```/g,
            (_match, language, code) => {
                const index = codeBlocks.length;
                const className = /^[a-zA-Z0-9+#.-]+$/.test(language) ? ` class="language-${language}"` : "";
                codeBlocks.push(`<pre><code${className}>${code.replace(/^\n|\n$/g, "")}</code></pre>`);
                return `\u0000CODE${index}\u0000`;
            },
        );

        const blocks = safeText.split(/\n{2,}/).map((block) => {
            if (/^\u0000CODE\d+\u0000$/.test(block.trim())) {
                return block.trim();
            }

            const heading = block.match(/^(#{1,3})\s+(.+)$/);
            if (heading) {
                const level = heading[1].length + 1;
                return `<h${level}>${formatInline(heading[2])}</h${level}>`;
            }

            const lines = block.split("\n");
            if (lines.every((line) => /^\s*[-*]\s+/.test(line))) {
                return `<ul>${lines.map((line) => `<li>${formatInline(line.replace(/^\s*[-*]\s+/, ""))}</li>`).join("")}</ul>`;
            }
            if (lines.every((line) => /^\s*\d+\.\s+/.test(line))) {
                return `<ol>${lines.map((line) => `<li>${formatInline(line.replace(/^\s*\d+\.\s+/, ""))}</li>`).join("")}</ol>`;
            }
            return `<p>${lines.map(formatInline).join("<br>")}</p>`;
        });

        return blocks.join("").replace(/\u0000CODE(\d+)\u0000/g, (_match, index) => codeBlocks[Number(index)]);
    }

    function addMessage(role, content, isLoading = false) {
        const row = document.createElement("div");
        row.className = `message ${role}`;

        const avatar = document.createElement("span");
        avatar.className = role === "assistant" ? "assistant-avatar" : "user-avatar";
        avatar.setAttribute("aria-hidden", "true");
        avatar.textContent = role === "assistant" ? "✦" : "You";
        row.appendChild(avatar);

        const body = document.createElement("div");
        body.className = "message-body";
        if (isLoading) {
            body.setAttribute("role", "status");
            body.setAttribute("aria-label", "StudyMate AI is thinking");
            body.innerHTML = '<span class="typing-indicator"><span></span><span></span><span></span></span>';
        } else if (role === "assistant") {
            body.innerHTML = renderMarkdown(content);
        } else {
            body.textContent = content;
        }
        row.appendChild(body);
        messagesElement.appendChild(row);
        messagesElement.scrollTop = messagesElement.scrollHeight;
        return row;
    }

    function setWaiting(waiting) {
        isWaiting = waiting;
        sendButton.disabled = waiting;
        clearButton.disabled = waiting;
        input.disabled = waiting;
        modeSelect.disabled = waiting;
        sendButton.setAttribute("aria-label", waiting ? "Waiting for StudyMate AI" : "Send message");
    }

    function getRecentMessages() {
        let totalLength = 0;
        const recent = [];
        for (let index = conversation.length - 1; index >= 0 && recent.length < 16; index -= 1) {
            const message = conversation[index];
            if (totalLength + message.content.length > 24000) {
                break;
            }
            recent.unshift(message);
            totalLength += message.content.length;
        }
        return recent;
    }

    async function sendMessage(message) {
        if (isWaiting || !message.trim()) {
            return;
        }

        const content = message.trim();
        input.value = "";
        input.style.height = "auto";
        starterPrompts.hidden = true;
        layout.classList.add("chat-active");
        addMessage("user", content);
        conversation.push({ role: "user", content });

        const loadingMessage = addMessage("assistant", "", true);
        setWaiting(true);

        try {
            const response = await fetch(chatUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    messages: getRecentMessages(),
                    mode: modeSelect.value,
                }),
            });
            const result = await response.json();
            loadingMessage.remove();

            if (!response.ok) {
                addMessage("assistant", result.error || "The request failed. Please try again.");
                return;
            }

            conversation.push({ role: "assistant", content: result.answer });
            addMessage("assistant", result.answer);
        } catch (_error) {
            loadingMessage.remove();
            addMessage("assistant", "Could not reach the StudyMate AI server. Check that the app is running and try again.");
        } finally {
            setWaiting(false);
            input.focus();
        }
    }

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        sendMessage(input.value);
    });

    input.addEventListener("input", () => {
        input.style.height = "auto";
        input.style.height = `${Math.min(input.scrollHeight, 180)}px`;
    });

    input.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            form.requestSubmit();
        }
    });

    starterPrompts.addEventListener("click", (event) => {
        const button = event.target.closest("[data-prompt]");
        if (!button || isWaiting) {
            return;
        }
        modeSelect.value = button.dataset.mode;
        input.value = button.dataset.prompt;
        input.focus();
        input.setSelectionRange(input.value.length, input.value.length);
        input.dispatchEvent(new Event("input"));
    });

    clearButton.addEventListener("click", () => {
        if (isWaiting) {
            return;
        }
        conversation.length = 0;
        messagesElement.replaceChildren();
        starterPrompts.hidden = false;
     layout.classList.remove("chat-active");
        addMessage(
            "assistant",
            "Hi! I can explain a topic, create notes or practice questions, and help you learn programming. What would you like to work on?",
        );
        modeSelect.value = "general";
        input.value = "";
        input.focus();
    });
})();
