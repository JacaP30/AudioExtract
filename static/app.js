const form = document.querySelector("#download-form");
const input = document.querySelector("#url");
const fileInput = document.querySelector("#file");
const feedback = document.querySelector("#feedback");
const button = form.querySelector("button[type='submit']");
const buttonLabel = button.querySelector(".button-label");

function isReady() {
  return Boolean(input.value.trim()) || Boolean(fileInput.files && fileInput.files.length);
}

function syncButton(busy = false) {
  const ready = isReady();
  button.disabled = busy || !ready;
  button.classList.toggle("is-busy", busy);
  buttonLabel.textContent = busy ? "Przetwarzanie" : "Pobierz audio";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!isReady()) {
    feedback.className = "feedback";
    feedback.textContent = "Wklej adres http/https albo wybierz plik z komputera.";
    return;
  }

  feedback.className = "feedback";
  feedback.textContent = "Wyciągam i konwertuję audio...";
  syncButton(true);

  try {
    const response = await fetch("/api/download", {
      method: "POST",
      body: new FormData(form),
    });

    if (!response.ok) {
      const result = await response.json();
      throw new Error(result.error || "Wystąpił nieoczekiwany błąd.");
    }

    const blob = await response.blob();
    const disposition = response.headers.get("Content-Disposition") || "";
    const match = disposition.match(/filename="?([^";]+)"?/i);
    const filename = match ? match[1] : "audio.mp3";
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    URL.revokeObjectURL(link.href);
    feedback.className = "feedback success";
    feedback.textContent = "Gotowe. Pobieranie pliku powinno już trwać.";
  } catch (error) {
    feedback.textContent = error.message;
  } finally {
    syncButton();
  }
});

input.addEventListener("input", () => syncButton());
fileInput.addEventListener("change", () => syncButton());
syncButton();
