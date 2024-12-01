document.addEventListener('DOMContentLoaded', () => {
    // Load saved settings from localStorage
    const contrastMode = localStorage.getItem('contrastMode');
    const textSize = localStorage.getItem('textSize');

    if (contrastMode === 'high') {
        document.body.classList.add('high-contrast');
    }

    if (textSize) {
        document.body.classList.add(`text-${textSize}`);
    }

    // Toggle High Contrast Mode
    document.getElementById('high-contrast-btn').addEventListener('click', () => {
        const body = document.body;
        body.classList.toggle('high-contrast');
        const mode = body.classList.contains('high-contrast') ? 'high' : 'normal';
        localStorage.setItem('contrastMode', mode);
    });

    // Adjust Text Size
    document.getElementById('text-small-btn').addEventListener('click', () => {
        updateTextSize('small');
    });

    document.getElementById('text-medium-btn').addEventListener('click', () => {
        updateTextSize('medium');
    });

    document.getElementById('text-large-btn').addEventListener('click', () => {
        updateTextSize('large');
    });

    function updateTextSize(size) {
        document.body.classList.remove('text-small', 'text-medium', 'text-large');
        document.body.classList.add(`text-${size}`);
        localStorage.setItem('textSize', size);
    }
});