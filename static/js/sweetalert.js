import Swal from "sweetalert2";
import Alpine from 'alpinejs';

document.addEventListener('alpine:init', () => {
    Alpine.data('notice', () => ({
        
        open: false,
    
        toggle() {
            console.log(this);
            this.open = ! this.open
        },
    }))
})

const Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 2000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.onmouseenter = Swal.stopTimer;
        toast.onmouseleave = Swal.resumeTimer;
    },
    html: `
        <button id="close-toast" class="swal2-close w-0 h-0" style="display: block; background-color: transparent; border: none; position: absolute; top: 0; right: 0;">&#x2715;</button>
    `,
    didRender: (toast) => {
        const closeButton = toast.querySelector('#close-toast');
        closeButton.addEventListener('click', () => {
            Swal.close();
        });
    }
});



window.Swal = Swal
window.Toast = Toast