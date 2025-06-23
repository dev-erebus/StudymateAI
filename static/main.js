document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('askForm');
  const queryInput = document.getElementById('query');
  const responseDiv = document.getElementById('response');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const query = queryInput.value.trim();
      if (!query) return;

      responseDiv.innerHTML = "<p>Thinking...</p>";

      try {
        const res = await fetch('/ai', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ query: query }),
        });

        const data = await res.json();
        if (data.response) {
          responseDiv.innerHTML = `<p>${data.response}</p>`;
        } else {
          responseDiv.innerHTML = `<p style="color:red;">${data.error || 'An unexpected error occurred.'}</p>`;
        }
      } catch (error) {
        responseDiv.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
      }
    });
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('darkToggle');

  // Apply saved mode on page load
  const savedMode = localStorage.getItem("darkMode");
  if (savedMode === "enabled") {
    document.body.classList.add("dark-mode");
    if (toggle) toggle.checked = true;
  }

  // Toggle listener
  if (toggle) {
    toggle.addEventListener('change', () => {
      if (toggle.checked) {
        document.body.classList.add("dark-mode");
        localStorage.setItem("darkMode", "enabled");
      } else {
        document.body.classList.remove("dark-mode");
        localStorage.setItem("darkMode", "disabled");
      }
    });
  }
});
