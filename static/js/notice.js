document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll('.notice-message');
    
    messages.forEach((element) => {
        const message = element.getAttribute('data-message');
        const messageTags = element.getAttribute('data-tags');

        if (messageTags.includes('success')) {
            iconType = 'success'
        } else if (messageTags.includes('error')) {
            iconType = 'error'
        } 
        Toast.fire({
            icon: iconType,
            title: message
        });
        element.remove();
    });
});
