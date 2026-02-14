document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    const resultDiv = document.getElementById('result');
    const radioButtons = document.querySelectorAll('input[name="inputType"]');
    const textInputSection = document.getElementById('text-input-section');
    const fileInputSection = document.getElementById('file-input-section');

    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'text') {
                textInputSection.style.display = 'block';
                fileInputSection.style.display = 'none';
            } else {
                textInputSection.style.display = 'none';
                fileInputSection.style.display = 'block';
            }
            resultDiv.innerHTML = ''; // Clear previous results
        });
    });

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        resultDiv.innerHTML = 'Classifying...';

        const formData = new FormData(form);
        const inputType = document.querySelector('input[name="inputType"]:checked').value;

        let url = '/predict';
        let options = {
            method: 'POST',
            body: formData
        };

        if (inputType === 'text') {
             options = {
                method: 'POST',
                body: new URLSearchParams(formData)
            };
        }
        
        fetch(url, options)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            } else if (data.prediction) {
                resultDiv.innerHTML = `<p><strong>Genre:</strong> ${data.prediction}</p>`;
            } else if (data.predictions) {
                let table = '<table><tr><th>Summary</th><th>Genre</th></tr>';
                data.predictions.forEach(item => {
                    table += `<tr><td>${item.summary.substring(0, 100)}...</td><td>${item.genre}</td></tr>`;
                });
                table += '</table>';
                resultDiv.innerHTML = table;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = `<p style="color: red;">An unexpected error occurred.</p>`;
        });
    });
});