import EasyMDE from 'simplemde';
import { marked } from 'marked';

function initializeEasyMDE() {
    const textareas = document.querySelectorAll('textarea.easymde');
    textareas.forEach(function(textarea) {
        new EasyMDE({
            element: textarea,
            toolbar: [
                "bold", 
                "italic", 
                "heading", 
                "|", 
                "quote", 
                "unordered-list", 
                "ordered-list", 
                "|", 
                "preview", 
                "|", 
                {
                    name: "guide",
                    action: function customFunction(editor) {
                        const win = window.open('https://simplemde.com/markdown-guide', '_blank');
                        if (win) {
                            win.focus();
                        }
                    },
                    className: "fa fa-info-circle",
                    title: "Markdown Guide",
                },
            ],
            previewRender: function(plainText) {
                return marked(plainText);
            }
        });
    });
}

function renderMarkdownPreview(elementId) {
    const descriptionElement = document.getElementById(elementId);
    if (descriptionElement) {
        let description = descriptionElement.getAttribute('data-description');
        if (description) {
            description = description.replace(/\\u000D\\u000A/g, '\n');
            descriptionElement.outerHTML = marked(description);
            console.log(descriptionElement.outerHTML);
        }
    }
}


document.addEventListener('DOMContentLoaded', (event) => {
    initializeEasyMDE();
    renderMarkdownPreview('description-preview');
});
