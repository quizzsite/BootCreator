function resizeIframe(width) {
	document.querySelector('.iframe-container').style.width = width + 'px';
}

function dragStart(event) {
	event.dataTransfer.setData("text/plain", event.target.innerHTML);
	event.dataTransfer.effectAllowed = "copy";
}

function allowDrop(event) {
	event.preventDefault();
	event.stopPropagation();
	const target = event.target.closest('.dropzone');
	if (target) {
		target.classList.add("dragover");
	}
}

function dragEnter(event) {
	event.preventDefault();
	event.stopPropagation();
	const target = event.target.closest('.dropzone');
	if (target) {
		target.classList.add("dragover");
	}
}

function dragLeave(event) {
	const target = event.target.closest('.dropzone');
	if (target) {
		target.classList.remove("dragover");
	}
}

function drop(event) {
	event.preventDefault();
	event.stopPropagation();
	const dropzone = event.target.closest('.dropzone');
	if (dropzone) {
		dropzone.classList.remove("dragover");
		const data = event.dataTransfer.getData("text");
		const newElement = document.createElement("div");
		newElement.classList.add("card");
		newElement.innerHTML = `<div class="card-body">${data}</div>`;
		dropzone.appendChild(newElement);

		// Send message to iframe
		const iframe = document.getElementById('myIframe');
		iframe.contentWindow.postMessage({ type: 'addElement', content: data }, '*');
	}
}
</script>