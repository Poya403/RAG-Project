
const resizer = document.getElementById("resizer");
const chatHistory = document.getElementById("ChatHistory");

let isResizing = false;

resizer.addEventListener("mousedown", function () {
    isResizing = true;
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";
});

document.addEventListener("mousemove", function (e) {

    if (!isResizing) return;

    const newWidth = window.innerWidth - e.clientX;

    if (newWidth >= 180 && newWidth <= 550) {
        chatHistory.style.width = newWidth + "px";
    }

});

document.addEventListener("mouseup", function () {

    isResizing = false;

    document.body.style.cursor = "default";
    document.body.style.userSelect = "auto";

});
