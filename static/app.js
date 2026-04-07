const form = document.getElementById("deal-form");
const resultEl = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());
  data.year = Number(data.year);
  data.mileage = Number(data.mileage);
  data.price = Number(data.price);
  data.accidents_count = Number(data.accidents_count || 0);
  data.owners_count = Number(data.owners_count || 1);
  data.condition = Number(data.condition || 3);

  if (!data.zip_code) {
    delete data.zip_code;
  }

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
    <p><strong>Estimated value:</strong> $${Number(payload.expected_price).toLocaleString()}</p>
    <p>${payload.reasoning}</p>
    <small>Confidence: ${(payload.confidence * 100).toFixed(0)}%</small>
  `;
});
