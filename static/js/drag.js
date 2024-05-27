import { Sortable } from '@shopify/draggable';
import Alpine from 'alpinejs';

function dragElement(element){
    const sortable = new Sortable(document.querySelectorAll('.mt-4'), {
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
    const items = Array.from(list.children);
    const positions = items.map((item, index) => {
        const id = item.dataset.id;
        console.log(`Item ID: ${id}, Position: ${index + 1}`);
        return { id: parseInt(id), position: index + 1 }; 
    });

    fetch('/resumes/update_positions/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ positions: positions }),
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        console.log('Positions updated successfully:', data);
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

console.log(Alpine)

document.addEventListener('alpine:init', () => {
    Alpine.data('draggable', () => ({
        init(){
            dragElement();
        }
    }))
})

