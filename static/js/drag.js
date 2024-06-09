import { Sortable } from '@shopify/draggable';
function dragElement(element){
    const sortable = new Sortable(document.querySelectorAll('.drag-container'), {
        draggable: '.drag',
    });

    sortable.on('drag:start', (evt) => {
        evt.data.source.classList.add('draggable--is-dragging');
    });

    sortable.on('sortable:sorted', (evt) => {
        evt.data.dragEvent.source.classList.remove('draggable--is-over');
        sendPositionUpdate(evt.data.dragEvent.source.parentElement);
    });
}


function sendPositionUpdate(list) {
    const items = Array.from(list.children).filter(item => item.classList.contains('drag'));
    const positions = items.map((item, index) => {
        const dataId = item.dataset.id;
        
        if (dataId) {
            const [type, id] = dataId.split('-');
            if(id){
                return { type, id: parseInt(id), position: index + 1 };
            }
        }
        return null;
    }).filter(item => item !== null);

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch('/resumes/update_positions/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ positions: positions }),
    });
}

document.addEventListener('DOMContentLoaded', () => {
    dragElement();
});
