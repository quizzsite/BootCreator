function dragEnter(event) {
    event.preventDefault();
    event.target.classList.add("dragover");
}

function dragLeave(event) {
    event.target.classList.remove("dragover");
}

function drop(event) {
    event.preventDefault();
    event.target.classList.remove("dragover");

    var data = event.dataTransfer.getData("text");
    var newElement = document.createElement("div");
    newElement.classList.add("card");
    newElement.innerHTML = `<div class="card-body">${data}</div>`;

    event.target.appendChild(newElement);
}

function dragStart(event) {
	event.dataTransfer.setData("text/plain", event.target.innerHTML);
	event.dataTransfer.effectAllowed = "copy";
}

function allowDrop(event) {
	event.preventDefault();
	event.target.classList.add("dragover");
}

function drop(event) {
	event.preventDefault();
	event.target.classList.remove("dragover");

	var data = event.dataTransfer.getData("text");
	var newElement = document.createElement("div");
	newElement.classList.add("card");
	newElement.innerHTML = `<div class="card-body">${data}</div>`;

	event.target.appendChild(newElement);
}
