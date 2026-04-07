from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="Car Deal Advisor API")
app.mount("/static", StaticFiles(directory="static"), name="static")


class EvaluateRequest(BaseModel):
    brand: str = Field(min_length=1)
    model: str = Field(min_length=1)
    year: int = Field(ge=1990, le=2030)
    mileage: int = Field(ge=0)
    price: float = Field(gt=0)
    zip_code: str | None = Field(default=None, min_length=5, max_length=10)
    accidents_count: int = Field(default=0, ge=0, le=20)
    owners_count: int = Field(default=1, ge=1, le=15)
    condition: int = Field(default=3, ge=1, le=5, description="1=poor, 5=excellent")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(Path("static/index.html"))


@app.post("/api/evaluate")
def evaluate_deal(payload: EvaluateRequest) -> dict:
    current_year = datetime.utcnow().year
    age = max(0, current_year - payload.year)

    # Baseline estimate. Replace with trained ML model once data integrations are live.
    estimated_base = 35000
    age_penalty = age * 1450
    mileage_penalty = (payload.mileage / 10000) * 850
    accidents_penalty = payload.accidents_count * 1000
    owner_penalty = max(0, payload.owners_count - 1) * 450
    condition_bonus = (payload.condition - 3) * 900

    expected_price = max(
        2500,
        estimated_base - age_penalty - mileage_penalty - accidents_penalty - owner_penalty + condition_bonus,
    )

    ratio = payload.price / expected_price
    if ratio <= 0.85:
        score = 92
        verdict = "Great deal"
    elif ratio <= 1.05:
        score = 80
        verdict = "Fair deal"
    elif ratio <= 1.20:
        score = 64
        verdict = "Slightly overpriced"
    else:
        score = 48
        verdict = "Overpriced"

    if payload.year >= current_year - 5:
        year_quality = "Strong recent model year"
    elif payload.year >= current_year - 10:
        year_quality = "Generally good model year"
    else:
        year_quality = "Older year: inspect service history carefully"

    confidence = 0.78
    if payload.accidents_count > 0:
        confidence -= 0.06
    if payload.owners_count >= 4:
        confidence -= 0.06
    if age > 12:
        confidence -= 0.08
    confidence = max(0.5, min(confidence, 0.92))

    reasoning = (
        f"Estimated value for this listing profile is around ${expected_price:,.0f}. "
        f"Listed at ${payload.price:,.0f}. "
        f"Inputs considered: age ({age} yrs), mileage, accidents ({payload.accidents_count}), "
        f"owners ({payload.owners_count}), and condition ({payload.condition}/5). "
        "Next step: verify VIN history, service records, and local comparable listings."
    )

    return {
        "model_type": "heuristic_baseline",
        "ml_enabled": False,
        "score": score,
        "verdict": verdict,
        "year_quality": year_quality,
        "reasoning": reasoning,
        "confidence": round(confidence, 2),
        "expected_price": round(expected_price, 2),
    }
