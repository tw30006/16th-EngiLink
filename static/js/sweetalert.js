import Swal from "sweetalert2";

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

showProcessingMessage = function(event) {
    Swal.fire({
        title: '處理中請稍候...',
        timer: 2000,
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading();
            const timer = Swal.getHtmlContainer().querySelector('b');
            timerInterval = setInterval(() => {
                timer.textContent = Swal.getTimerLeft();
            }, 100);
            event.target.submit();
        },
        willClose: () => {
            clearInterval(timerInterval);
        }
    });
}

window.Swal = Swal
window.Toast = Toast
