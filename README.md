# Car Deal Advisor (AI-Powered)

A starter project for a professional website that helps users decide whether a used car listing is a good deal.

## What this app does

Users enter:
- Brand
- Model
- Year
- Mileage
- Price (USD)
- Optional trust/condition signals (ZIP, accidents, owners, condition)

The app returns:
- **Deal score** (0-100)
- **Deal verdict** (Great / Fair / Overpriced)
- **Model year confidence**
- **Estimated value** and reasoning

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open: http://127.0.0.1:8000

## How to use machine learning with KBB, Edmunds, and CARFAX for higher accuracy

> Important: KBB, Edmunds, and CARFAX data is proprietary. Use official partnerships/licensed APIs and follow contract terms.

### 1) Build a training dataset
For each sold/listed vehicle row, gather:
- `make, model, trim, year, mileage, drivetrain, fuel, transmission, body_type`
- `zip_code / metro`
- `list_price` and if available `sale_price`
- CARFAX history features: `accident_count`, `damage_severity`, `owners_count`, `fleet_or_rental`, `title_flags`, `service_record_count`
- KBB/Edmunds valuation features: `kbb_fair_value`, `edmunds_market_value`, percentile ranges
- Time features: `listing_date`, seasonality, days-on-market

### 2) Feature engineering
- Vehicle age (`current_year - year`)
- Miles-per-year (`mileage / age`)
- Region adjustments (ZIP-level demand/supply)
- Reliability priors by model-year (failure/recall history)
- Condition/historical risk score from CARFAX-derived fields

### 3) Modeling strategy
Use two models:
1. **Price model** (regression): predict fair value. Start with XGBoost/LightGBM/CatBoost.
2. **Quality risk model** (classification): predict probability of expensive issues within 12 months.

Then combine into a final score:

```text
deal_score = 0.7 * price_advantage_score + 0.3 * reliability_score
```

Where:
- `price_advantage_score` depends on `(predicted_fair_price - asking_price) / predicted_fair_price`
- `reliability_score` is higher when risk model predicts lower defect probability.

### 4) Evaluation
Track:
- Regression: MAE, MAPE by brand/model/year segment
- Classification: AUC-ROC, precision@k for high-risk flags
- Calibration: reliability curves for risk probabilities

### 5) Production serving
- Keep current heuristic as fallback.
- Add a `model_version` to API responses.
- Retrain monthly and monitor drift by ZIP + make/model cohorts.
- Add guardrails to prevent overconfident outputs on sparse segments.

### 6) Compliance and trust
- Show “why this score” with top factors (SHAP/feature importance).
- Include data recency badges.
- Add clear disclaimer: guidance only, not legal/financial/mechanical advice.

## API

### `POST /api/evaluate`

Request example:

```json
{
  "brand": "Toyota",
  "model": "Camry",
  "year": 2018,
  "mileage": 65000,
  "price": 17000,
  "zip_code": "60614",
  "accidents_count": 0,
  "owners_count": 2,
  "condition": 4
}
```

Response fields include:
- `score`
- `verdict`
- `year_quality`
- `expected_price`
- `confidence`
- `reasoning`

## Disclaimer

This tool provides guidance only and should not be treated as legal, mechanical, or financial advice.


## Is machine learning enabled right now?

No. The current implementation uses a deterministic heuristic baseline (rule-based calculation), not a trained ML model.

Current state:
- `ml_enabled = false` in API response
- `model_type = "heuristic_baseline"`
- KBB/Edmunds/CARFAX ML section is a production roadmap, not active code yet

To enable real ML, you would add a trained model artifact and model inference path in `POST /api/evaluate`.
