import EasyMDE from 'simplemde';
import marked from 'marked';

function initializeEasyMDE() {
    const textarea = document.querySelector('textarea[name="skills"]');
    if (textarea) {
        const easyMDE = new EasyMDE({
            element: textarea,
            toolbar: [
                "bold", "italic", "heading", "|",
                "quote", "unordered-list", "ordered-list", "|",
                "preview", "|",
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
    } 
}


document.addEventListener('DOMContentLoaded', (event) => {
    initializeEasyMDE();
});
