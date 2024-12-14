document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.getElementById('theme-toggle');
  const body = document.body;

  // Handle theme toggle
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark-mode') {
    body.classList.add('dark-mode');
    themeToggle.textContent = 'Switch to Light Mode';
  }

  themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    const isDarkMode = body.classList.contains('dark-mode');
    themeToggle.textContent = isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    localStorage.setItem('theme', isDarkMode ? 'dark-mode' : 'light-mode');
  });

  // Handle avatar upload
  const avatarImg = document.getElementById('avatar');
  const uploadInput = document.getElementById('upload-avatar');
  const uploadBtn = document.getElementById('upload-btn');
  const removeBtn = document.getElementById('remove-btn');

  // Event listener for upload button
  uploadBtn.addEventListener('click', () => {
    uploadInput.click(); // Trigger file input click
  });

  // Event listener for file input change
  uploadInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        avatarImg.src = e.target.result; // Update avatar image
        localStorage.setItem('avatar', e.target.result); // Save avatar to localStorage
      };
      reader.readAsDataURL(file);
    }
  });

  // Event listener for remove button
  removeBtn.addEventListener('click', () => {
    avatarImg.src = 'default-avatar.jpg'; // Reset to default avatar
    localStorage.removeItem('avatar'); // Remove avatar from localStorage
  });

  // Load avatar from localStorage on page load
  const savedAvatar = localStorage.getItem('avatar');
  if (savedAvatar) {
    avatarImg.src = savedAvatar;
  }
});
