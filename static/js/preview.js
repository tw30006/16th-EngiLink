document.querySelector('input[type="file"]').addEventListener('change', function(event) {
  const file = event.target.files[0];
  if (file) {
      const reader = new FileReader();
      reader.onload = function(e) {
          const previewContainer = document.getElementById('preview-container');
          const previewImage = document.getElementById('preview');
          previewImage.src = e.target.result;
          previewContainer.style.display = 'block';
      };
      reader.readAsDataURL(file);
  }
});