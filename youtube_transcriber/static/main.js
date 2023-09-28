function summarizeVideo() {
    const videoUrl = document.getElementById('videoUrl').value;

    fetch('/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ youtube_url: videoUrl }),
    })
    .then(response => response.json())
    .then(data => {
        const resultElement = document.getElementById('result');
        resultElement.innerHTML = `<h2>Summarized Transcript:</h2><p>${data.summarized_text}</p>`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Attach the event listener to the button
document.getElementById('summarizeButton').addEventListener('click', summarizeVideo);
