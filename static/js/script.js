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

  // Avatar upload button behavior
  const uploadInput = document.getElementById('upload-avatar');
  const uploadBtn = document.getElementById('upload-btn');

  uploadBtn.addEventListener('click', () => {
    uploadInput.click(); // Trigger file input click
  });
});
