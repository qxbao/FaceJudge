// You should disable CORS in your browser or use a CORS extension to make this script work.
// Recommendation: https://github.com/PhilGrayson/chrome-csp-disable

const floatingForm = document.createElement('form');
floatingForm.style = `
    display: flex;
    position: fixed;
    bottom: 20px;
    right: 50%;
    transform: translateX(50%);
    width: 300px;
    background-color: #f9f9f9;
    border: 1px solid #ccc;
    z-index: 1000;`
floatingForm.innerHTML = `
    <input type="number" min="0" max="100" placeholder="Score"
    style="flex-grow: 1; padding: 10px; box-sizing: border-box;">
    <button type="submit" style="padding: 10px; box-sizing: border-box; background-color: blue; color: white;">Judge</button>
    `
floatingForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const scoreInput = floatingForm.querySelector('input[type="number"]');
    const score = parseInt(scoreInput.value, 10);
    const age = document.querySelector('.encounters-user').querySelector('.encounters-story-profile__age').textContent.split(",")[1].trim();
    if (isNaN(score) || score < 0 || score > 100) {
        alert('Please enter a valid score between 0 and 100.');
        return;
    }
    const base64Images = []
    const images = Array.from(document.querySelector('.encounters-user').querySelectorAll('img.media-box__picture-image'));
    images.pop();
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    for (const image of images) {
        image.crossOrigin = 'anonymous';
        canvas.width = image.naturalWidth;
        canvas.height = image.naturalHeight;
        ctx.drawImage(image, 0, 0);
        base64Images.push(canvas.toDataURL('image/png'));
    }
    for (const image of base64Images) {
        if (!image.startsWith('data:image/png;base64,')) {
            console.error('Invalid image format:', image);
            return;
        }
    }
    const data = {
        score,
        age,
        images: base64Images
    };
    console.log('Sending data to server:', data);
    fetch('http://localhost:5000/judge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from server:', data);
        if (data.error) {
            console.error(data.error);
            floatingForm.style.borderColor = 'red';
        } else {
            floatingForm.style.borderColor = 'green';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        floatingForm.style.borderColor = 'red';
    });
    setTimeout(() => {
        floatingForm.style.borderColor = '#ccc';
    }, 3000);
    scoreInput.value = '';
})

document.body.appendChild(floatingForm);