# Car Deal Advisor (AI-Powered)

A starter project for a professional website that helps users decide whether a used car listing is a good deal.

## What this app does

Users enter:
- Brand
- Model
- Year
- Mileage
- Price (USD)

The app returns:
- **Deal score** (0-100)
- **Deal verdict** (Great / Fair / Overpriced)
- **Model year confidence** (how reliable that year appears)
- Short reasoning and next-step suggestions.

## Why this is useful

Shoppers can quickly evaluate listings before spending time contacting sellers, while still getting transparency about *why* a car is scored a certain way.

## Architecture

- **Frontend**: HTML/CSS/vanilla JS (replaceable with React/Next.js later).
- **Backend**: FastAPI service with:
  - deterministic baseline scoring rules
  - optional LLM explanation layer via OpenAI API
- **Future data integrations**:
  - market pricing APIs (KBB, Edmunds, Cars.com datasets, etc.)
  - reliability sources (NHTSA recalls, Consumer Reports, owner forums)

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open: http://127.0.0.1:8000

## API

### `POST /api/evaluate`

Request:

```json
{
  "brand": "Toyota",
  "model": "Camry",
  "year": 2018,
  "mileage": 65000,
  "price": 17000
}
```

Response:

```json
{
  "score": 78,
  "verdict": "Fair deal",
  "year_quality": "Good model year",
  "reasoning": "Price is slightly above expected market value, but mileage is reasonable for age.",
  "confidence": 0.73
}
```

## Production roadmap

1. **MVP (2-4 weeks)**
   - collect listing inputs
   - scoring + explanation
   - shareable result page
2. **Data enrichment (4-8 weeks)**
   - market comps by ZIP code
   - title/accident checks via partner APIs
3. **Trust & growth**
   - “why this score” transparency panel
   - saved searches, email alerts
   - monetization via affiliate leads/dealer referrals

## Important disclaimer

This tool provides guidance only and should not be treated as legal, mechanical, or financial advice.
