const Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.onmouseenter = Swal.stopTimer;
        toast.onmouseleave = Swal.resumeTimer;
    },
    // Add html property to include close button
    html: `
        <div>
            <div id="toast-message"></div>
            <button id="close-toast" class="swal2-close" style="display: block; background-color: transparent; border: none; position: absolute; top: 0; right: 0;">&#x2715;</button>
        </div>
    `,
    // Event listener for the close button
    didRender: (toast) => {
        const closeButton = toast.querySelector('#close-toast');
        closeButton.addEventListener('click', () => {
            Swal.close();
        });
    }
});
