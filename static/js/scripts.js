document.addEventListener('DOMContentLoaded', function() {
    let counter = 0;
    const button = document.getElementById('counterButton');
    const counterDisplay = document.getElementById('counter');

    button.addEventListener('click', function() {
        counter++;
        counterDisplay.textContent = counter;
    });
});