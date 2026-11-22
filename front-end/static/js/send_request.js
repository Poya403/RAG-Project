const questionInput = document.getElementById("question-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");


// Send question to Flask
async function askQuestion() {

    const question = questionInput.value.trim();

    // Check empty question
    if (!question) {
        return;
    }

    // Display user's question
    const userMessage = document.createElement("p");
    userMessage.className = "user-message";
    userMessage.textContent = question;

    chatMessages.appendChild(userMessage);

    // Clear input
    questionInput.value = "";

    // Show loading message
    const loadingMessage = document.createElement("p");
    loadingMessage.className = "bot-message";
    loadingMessage.textContent = "در حال پردازش سوال...";
    
    chatMessages.appendChild(loadingMessage);

    // Disable send button
    sendButton.disabled = true;

    try {

        // Send question to Flask
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        // Remove loading message
        loadingMessage.remove();

        if (!response.ok) {
            throw new Error(data.error || "خطا در دریافت پاسخ");
        }

        // Display RAG answer
        const botMessage = document.createElement("p");
        botMessage.className = "bot-message";
        botMessage.textContent = data.answer;

        chatMessages.appendChild(botMessage);

    } catch (error) {

        loadingMessage.remove();

        const errorMessage = document.createElement("p");
        errorMessage.className = "bot-message error-message";
        errorMessage.textContent = "خطا: " + error.message;

        chatMessages.appendChild(errorMessage);

        console.error(error);

    } finally {

        // Enable send button
        sendButton.disabled = false;
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
