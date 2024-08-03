function createCard(widgetName) {
    const card = document.createElement('div');
    card.className = 'card';
    card.draggable = true;
    card.addEventListener('dragstart', dragStart);

    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';
    cardBody.textContent = widgetName;

    card.appendChild(cardBody);
    return card;
}

function drop(event) {
    event.preventDefault();
    event.target.classList.remove("dragover");

    const dropzone = event.target.closest('.dropzone');
    if (dropzone) {
        const data = event.dataTransfer.getData("text/plain");
        const newElement = document.createElement("div");
        newElement.classList.add("card");
        newElement.innerHTML = `<div class="card-body">${data}</div>`;

        const iframe = dropzone.querySelector('iframe');
        if (iframe) {
            const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
            const insertionLine = iframeDocument.getElementById('insertion-line');

            if (insertionLine && insertionLine.parentElement) {
                iframeDocument.body.insertBefore(newElement, insertionLine.nextSibling);
            } else {
                iframeDocument.body.appendChild(newElement);
            }
        }
    }
    hideInsertionLine();
    document.getElementsByClassName("dropzone")[0].classList.remove("dragover");
}

document.addEventListener('DOMContentLoaded', () => {
    initializeSidebar();

    const dropzone = document.querySelector('.dropzone');
    const iframe = document.getElementById('editor');
    const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
    iframeDocument.body.innerHTML = '<div style="height: 100%;"></div>'; // Initialize iframe body
    const insertionLine = document.createElement('div');
    insertionLine.id = 'insertion-line';
    insertionLine.style.position = 'absolute';
    insertionLine.style.height = '2px';
    insertionLine.style.backgroundColor = 'white';
    insertionLine.style.display = 'none';
    iframeDocument.body.appendChild(insertionLine);

    dropzone.addEventListener('dragover', allowDrop);
    dropzone.addEventListener('drop', drop);
    dropzone.addEventListener('dragenter', dragEnter);
    dropzone.addEventListener('dragleave', dragLeave);

    iframeDocument.addEventListener('dragover', (event) => {
        event.preventDefault();
        showInsertionLine(iframeDocument, event.clientY);
    });

    iframeDocument.addEventListener('drop', (event) => {
        event.preventDefault();
        hideInsertionLine();

        const data = event.dataTransfer.getData("text/plain");
        const newElement = document.createElement("div");
        newElement.classList.add("card");
        newElement.innerHTML = `<div class="card-body">${data}</div>`;
        iframeDocument.body.appendChild(newElement);
    });

    iframeDocument.addEventListener('dragenter', (event) => {
        event.preventDefault();
        showInsertionLine(iframeDocument, event.clientY);
    });

    iframeDocument.addEventListener('dragleave', (event) => {
        hideInsertionLine();
    });
});

function initializeSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const widgetNames = ['Navigation', 'Headers', 'Features'];

    widgetNames.forEach(widgetName => {
        const card = createCard(widgetName);
        sidebar.appendChild(card);
    });
}

function dragStart(event) {
    event.dataTransfer.setData("text/plain", event.target.innerHTML);
    event.dataTransfer.effectAllowed = "copy";
}

function allowDrop(event) {
    event.preventDefault();
    document.getElementsByClassName("dropzone")[0].classList.add("dragover");
}

function dragEnter(event) {
    event.preventDefault();
    document.getElementsByClassName("dropzone")[0].classList.add("dragover");
}

function dragLeave(event) {
    document.getElementsByClassName("dropzone")[0].classList.remove("dragover");
}

function showInsertionLine(iframeDocument, yPosition) {
    const insertionLine = iframeDocument.getElementById('insertion-line');
    insertionLine.style.top = yPosition + 'px';
    insertionLine.style.display = 'block';
}

function hideInsertionLine() {
    const iframe = document.getElementById('editor');
    const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
    const insertionLine = iframeDocument.getElementById('insertion-line');
    insertionLine.style.display = 'none';
}
