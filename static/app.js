const form = document.getElementById("deal-form");
const resultEl = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());
  data.year = Number(data.year);
  data.mileage = Number(data.mileage);
  data.price = Number(data.price);

  const response = await fetch("/api/evaluate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const payload = await response.json();

  resultEl.classList.remove("hidden");
  resultEl.innerHTML = `
    <h2>${payload.verdict} (Score: ${payload.score}/100)</h2>
    <p><strong>Model year:</strong> ${payload.year_quality}</p>
    <p>${payload.reasoning}</p>
    <small>Confidence: ${(payload.confidence * 100).toFixed(0)}%</small>
  `;
});
