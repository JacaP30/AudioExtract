const form = document.querySelector("#download-form");
const input = document.querySelector("#url");
const feedback = document.querySelector("#feedback");
const button = form.querySelector("button");
const buttonLabel = button.querySelector(".button-label");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  feedback.className = "feedback";
  feedback.textContent = "Pobieram i konwertuję audio...";
  button.disabled = true;
  buttonLabel.textContent = "Przetwarzanie";

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
    button.disabled = false;
    buttonLabel.textContent = "Pobierz audio";
  }
});