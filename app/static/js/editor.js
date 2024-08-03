var socket = io.connect('http://localhost:5000');

socket.on('connect', function() {
        let urlParts = document.location.href.split('/');
        socket.emit('update_project', {
        proj: urlParts[length - 1],
        file: 'index.html',
        s: []
    });
});

socket.on('update_response', function(url) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();  // Преобразуем ответ в текст
        })
        .then(data => {
            document.getElementById('editor').contentDocument.write(data);
            document.getElementById('editor').contentDocument.close();
            document.getElementById('editor').contentDocument.addEventListener('click', showIt);
        })
        .catch(error => {
            console.error('Error fetching the file:', error);
        });
});

function showIt(e)
{
	console.log(e.target);
}