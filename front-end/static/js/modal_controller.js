function openRenameModal(conversationId, currentTitle) {
    selectedConversationId = conversationId;

    newTitleInput.value = currentTitle;
    renameModal.style.display = "flex";
}

function closeRenameModal() { renameModal.style.display = "none"; }

document.getElementById("cancel-rename").addEventListener("click", closeRenameModal);