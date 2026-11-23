let currentConversationId = null;
let selectedConversationId = null;

// functions
async function getConversationTitles(){
    try {
        const response = await fetch("/conversations");
        const data = await response.json();

        if(!response.ok){
            throw new Error(data.error || "Failed to retrieve conversations.");
        }

        return data;

    } catch(error){
        console.error(error);
        return [];
    }
}

async function getConversationMessages(conversationId) {
    try {
        const response = await fetch(`/conversations/${conversationId}`);

        const messages = await response.json();

        if (!response.ok) {
            throw new Error(messages.error || "Failed to retrieve messages.");
        }

        return messages;

    } catch (error) {
        console.error("Error loading conversation:", error);
        return null;
    }
}

async function displayConversationTitles() {
    const conversations = await getConversationTitles();

    if(conversations.length === 0)
        console.log("No conversation found!")

    conversationTitles.innerHTML = "";

    conversations.forEach(conversation => {
        const title = document.createElement("div");

        title.classList.add("conversation-title");

        title.dataset.conversationId = conversation.id;
        title.innerHTML = `
            <div class="conversation-actions">
                <button class="more-btn">⋯</button>

                <div class="action-menu">
                    <button class="rename-btn">
                        <i class="fa-solid fa-pen"></i>
                    </button>
                    <button class="delete-btn">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </div>
            <span class="title-text">${conversation.title}</span>
            `
        conversationTitles.appendChild(title);
    });
}

async function loadConversation(conversationId) {

    // Prevent loading while processing a question
    if (isProcessing) return;

    const messages = await getConversationMessages(conversationId);

    if (messages === null) return;

    // Clear previous messages
    chatMessages.innerHTML = "";

    // Set current conversation
    currentConversationId = Number(conversationId);

    // Update chat layout
    chat.classList.add("chat-started");
    welcomeMessage.hidden = true;

    // Display retrieved messages
    messages.forEach(message => {

        const messageElement = document.createElement("p");

        if (message.role === "user") {
            messageElement.className = "user-message";
        } else {
            messageElement.className = "bot-message";
        }

        messageElement.textContent = message.content;

        chatMessages.appendChild(messageElement);
    });

    scrollToBottom();
}

async function addConversation() {
    try {
        const response = await fetch("/addConversation", {method: "POST"});
        
        if (!response.ok) { throw new Error("Failed to create conversation"); }

        const conversation = await response.json();
        currentConversationId = conversation.conversation_id;

        await displayConversationTitles();
        
        return currentConversationId;

    } catch (error) {
        console.error("Error creating conversation:", error);
    }
}

async function deleteConversation(conversationId) {
    try {
        const response = await fetch("/deleteConversation", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                conversation_id: conversationId
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to delete conversation.");
        }

        console.log("Conversation deleted:", data);

        return true;

    } catch (error) {
        console.error("Error deleting conversation:", error);
        return false;
    }
}

async function renameConversation(conversationId, newTitle) {
    try {
        const response = await fetch("/renameConversation", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                new_title: newTitle
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to rename conversation.");
        }

        return true;

    } catch (error) {
        console.error("Error renaming conversation:", error);
        return false;
    }
}

function startNewChat() {
    chatMessages.innerHTML = "";
    currentConversationId = null;
    welcomeMessage.hidden = false;
    chat.classList.remove("chat-started");
    questionInput.value = "";
    updateSendButton();
}

//--------------

//events
newChatButton.addEventListener("click", startNewChat);
document.addEventListener("click", function(event) {
    const moreButton = event.target.closest(".more-btn");

    // Close all active menus
    document.querySelectorAll(".conversation-title.active")
        .forEach(title => {
            title.classList.remove("active");
        });

    // Open selected menu
    if (moreButton) {
        event.stopPropagation();
        const conversation = moreButton.closest(".conversation-title");
        conversation.classList.add("active");
    }
});
conversationTitles.addEventListener("click", async function(event) {
    if (event.target.closest(".delete-btn")) {
        const conversationTitle = event.target.closest(".conversation-title");
        const conversationId = conversationTitle.dataset.conversationId;

        const deleted = await deleteConversation(conversationId);

        if (deleted) conversationTitle.remove();
    }

});
conversationTitles.addEventListener("click", function(event) {
    if (event.target.closest(".rename-btn")) {
        const conversationTitle = event.target.closest(".conversation-title");

        const conversationId = conversationTitle.dataset.conversationId;

        const currentTitle = conversationTitle.querySelector(".title-text").textContent;

        openRenameModal(conversationId, currentTitle);
    }
});
document.getElementById("confirm-rename").addEventListener("click", async function() {
    const newTitle = newTitleInput.value.trim();

    if (!newTitle) return;

    const renamed = await renameConversation(selectedConversationId, newTitle);

    if (renamed) {
        const conversationTitle = document.querySelector(
            `.conversation-title[data-conversation-id="${selectedConversationId}"]`
        );

        conversationTitle.querySelector(".title-text").textContent = newTitle;
        renameModal.style.display = "none";
    }

});
conversationTitles.addEventListener("click", function(event) {

    // Ignore clicks on conversation actions
    if (event.target.closest(".conversation-actions")) return;

    const conversationTitle = event.target.closest(".conversation-title");

    if (!conversationTitle) return;

    const conversationId = conversationTitle.dataset.conversationId;

    loadConversation(conversationId);
});
//---------------
displayConversationTitles();