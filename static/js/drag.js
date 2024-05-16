document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded event fired');
    console.log('Draggable:', window.Draggable);
    if (window.Draggable) {
        const Sortable = window.Draggable.Sortable;
        const sortable = new Sortable(document.querySelectorAll('ul'), {
        draggable: 'p',
    });
    sortable.on('drag:start', (evt) => {
        evt.data.source.classList.add('draggable--is-dragging');
    });

    sortable.on('drag:stop', (evt) => {
        evt.data.source.classList.remove('draggable--is-dragging');
    });

    sortable.on('sortable:sort', (evt) => {
        evt.data.dragEvent.source.classList.add('draggable--is-over');
    });

    sortable.on('sortable:sorted', (evt) => {
        evt.data.dragEvent.source.classList.remove('draggable--is-over');
    });
    } else {
        console.error('Draggable is not loaded');
    }
});

