const form = document.getElementById('file-upload-form');
form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
		const formData = new FormData();
		formData.append('file', file);
		try {
		    const response = await fetch('/upload', {
		        method: 'POST',
		        body: formData
		    });
		    if (!response.ok) {
		        throw new Error(response.statusText);
		    }
		    const files = await response.json();
		    const fileList = document.getElementById('file-list');
		    fileList.innerHTML = `<table id="file-list"><thead><tr><th><a href="{{ url_for('sort_files', sort_by='name', sort_order='asc') }}">Name</a></th><th>Mime</th><th><a href="{{ url_for('sort_files', sort_by='upload_time', sort_order='asc') }}">Uploaded</a></th><th><a href="{{ url_for('sort_files', sort_by='size', sort_order='asc') }}">Size</a></th><th>^_+_^</th><th><--X--></th></tr></thead>`;
		    files.forEach(file => {
		        const fileRow = document.createElement('tr');
		        fileRow.innerHTML = `<td>${file.name}</td><td>${file.mimetype}</td><td>${file.upload_time}</td><td>${file.size}</td>`;
		        fileList.appendChild(fileRow);
		    });
		} catch (error) {
		    console.error(error);
		}
		form.reset();
});
