let isProcessing = false;

// Update send button state
function updateSendButton() {
    sendButton.disabled =
        questionInput.value.trim() === "" || isProcessing;
}
// Update button when input changes
questionInput.addEventListener("input", updateSendButton);

// Auto scroll to latest message
function scrollToBottom() {
    chatContent.scrollTop = chatContent.scrollHeight;
}

// Display retrieved sources
function displaySources(sources) {
    if (!sources || sources.length === 0)  return;

    // Create sources container
    const sourcesContainer = document.createElement("div");
    sourcesContainer.className = "sources-container";

    // Create sources title
    const sourcesTitle = document.createElement("h3");
    sourcesTitle.textContent = "مستندات مرتبط با پاسخ";

    sourcesContainer.appendChild(sourcesTitle);

    // Display each retrieved chunk
    sources.forEach((source, index) => {
        const sourceElement = document.createElement("div");
        sourceElement.className = "source-item";

        const sourceTitle = document.createElement("h4");
        sourceTitle.textContent = `مستند ${index + 1}`;

        const sourceText = document.createElement("p");
        sourceText.textContent = source;

        sourceElement.appendChild(sourceTitle);
        sourceElement.appendChild(sourceText);

        sourcesContainer.appendChild(sourceElement);
    });

    chatMessages.appendChild(sourcesContainer);

    scrollToBottom();
}

// Send question to Flask
async function askQuestion() {
    const question = questionInput.value.trim();

    // Check empty question
    if (!question || isProcessing) return;

    isProcessing = true;
    updateSendButton();

    // Change chat layout
    chat.classList.add("chat-started");

    // Hide welcome message
    welcomeMessage.hidden = true;

    // Display user's question
    const userMessage = document.createElement("p");
    userMessage.className = "user-message";
    userMessage.textContent = question;

    chatMessages.appendChild(userMessage);

    // Clear input
    questionInput.value = "";

    // Create bot message
    const answerElement = document.createElement("p");
    answerElement.className = "bot-message";
    answerElement.textContent = "در حال پردازش سوال...";

    chatMessages.appendChild(answerElement);

    // Scroll to latest message
    scrollToBottom();

    // Disable send button
    sendButton.disabled = true;

    try {
        // Create a new conversation if none exists
        if (currentConversationId === null) {
            await addConversation();
        }

        // Send question to Flask
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question,
                conversation_id: currentConversationId
            })
        });

        // Check response status
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "خطا در دریافت پاسخ");
        }

        // Read streaming response
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        let retrievedSources = [];
        let buffer = "";

        answerElement.textContent = "";

        function processLine(line) {
            if (!line.trim()) {
                return;
            }

            const event = JSON.parse(line);

            if (event.type === "sources") {
                retrievedSources = event.sources;
            }

            else if (event.type === "token") {
                answerElement.textContent += event.content;
                scrollToBottom();
            }
        }

        while (true) {
            const {value, done} = await reader.read();

            if (done) break;

            buffer += decoder.decode(value, {stream: true});

            const lines = buffer.split("\n");

            buffer = lines.pop();

            for (const line of lines) processLine(line);
        }

        buffer += decoder.decode();

        if (buffer.trim()) 
            processLine(buffer);

        displaySources(retrievedSources);
        scrollToBottom();

    } catch (error) {
        answerElement.textContent = "خطا: " + error.message;
        answerElement.classList.add("error-message");
        console.error(error);

    } finally {
        isProcessing = false;
        updateSendButton();
        questionInput.focus();
    }
}

// Connect button to askQuestion
sendButton.addEventListener("click", askQuestion);

// Send question by pressing Enter
questionInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        askQuestion();
    }
});

updateSendButton();