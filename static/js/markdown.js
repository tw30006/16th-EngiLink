import { marked } from 'marked';

document.addEventListener('DOMContentLoaded', function () {
    const markdownElements = document.querySelectorAll('.markdown-content');
    markdownElements.forEach(function(element) {
        const markdownText = element.innerText; 
        const htmlContent = marked(markdownText); 
        element.innerHTML = htmlContent; 
    });

});
