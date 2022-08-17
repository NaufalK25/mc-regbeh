// Get color for server status
const statusArticle = document.querySelector(".main_header_desc_status");
const serverStatusColor = statusArticle.dataset.color;

const serverStatusMessage = document.querySelector(".server_status_message");
serverStatusMessage.style.color = serverStatusColor;

const serverStatusCircle = document.querySelector(".server_status_circle");
serverStatusCircle.style.backgroundColor = serverStatusColor;

// show copy to clipboard message
const copyToClipboardIcon = document.querySelector(
    ".main_header_desc_footer>svg"
);
const regbehMinecraftServer = document.querySelector(
    ".main_header_desc_footer>p"
);

const createAlert = (message) => {
    const alert = document.createElement("p");
    alert.innerText = message;
    alert.classList.add("alert");

    document.body.appendChild(alert);

    removeAlert(alert);
};

const removeAlert = (alert) => {
    alert.addEventListener("click", () => {
        alert.remove();
    });

    setTimeout(() => {
        alert.remove();
    }, 2000);
};

copyToClipboardIcon.addEventListener("click", () => {
    navigator.clipboard.writeText(regbehMinecraftServer.innerText);

    createAlert("Copied to clipboard");
});
