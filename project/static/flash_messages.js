document.addEventListener("DOMContentLoaded", function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        message.classList.add('show');
        setTimeout(function() {
            message.classList.remove('show');
            message.classList.add('hide');
        }, 3000); // Show for 3 seconds
        setTimeout(function() {
            message.remove();
        }, 3500); // Remove from DOM after animation
    });
});
