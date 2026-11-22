
const chat = document.getElementById("Chat");
const chatContent = document.getElementById("chat-content");

const questionInput = document.getElementById("question-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");
const welcomeMessage = document.getElementById("welcome-msg");


// Auto scroll to latest message
function scrollToBottom() {
    chatContent.scrollTop = chatContent.scrollHeight;
}


// Send question to Flask
async function askQuestion() {

    const question = questionInput.value.trim();

    // Check empty question
    if (!question) {
        return;
    }

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

        // Check response status
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "خطا در دریافت پاسخ");
        }

        // Read streaming response
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        // Clear loading message
        answerElement.textContent = "";

        while (true) {

            const { value, done } = await reader.read();

            if (done) break;

            const token = decoder.decode(value, {
                stream: true
            });

            answerElement.textContent += token;

            // Auto scroll during streaming
            scrollToBottom();
        }

        // Decode remaining characters
        answerElement.textContent += decoder.decode();

        scrollToBottom();

    } catch (error) {

        answerElement.textContent = "خطا: " + error.message;

        answerElement.classList.add("error-message");

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
