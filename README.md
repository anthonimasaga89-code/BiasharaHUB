# Biashara HUB Backend

Production-oriented FastAPI backend foundation for Biashara HUB: business management, products, AI content, social integrations, publishing, orders, payments architecture, analytics, and ML.

## Stack

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy (classic `Column` style)
- Alembic
- Pydantic Settings
- JWT
- OAuth 2.0
- pytest
- scikit-learn

## Architecture

```text
Route
  -> Service
      -> Database / Integration / AI / ML
```

External providers are isolated under `app/integrations/`.

## Run locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Set a PostgreSQL `DATABASE_URL` in `.env`, then run:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Swagger: `http://localhost:8000/docs`

Health: `http://localhost:8000/health`

## Authentication

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `POST /api/auth/logout`
- `GET /api/auth/me`

## Business and products

- Business CRUD under `/api/businesses`
- Product CRUD under `/api/products`

Ownership checks prevent one business owner from managing another owner's resources.

## Social media

Supported architecture:

- LinkedIn
- Instagram
- Facebook
- WhatsApp
- TikTok
- X

Provider credentials belong in `.env` only. Tokens are never returned in normal SocialAccount responses.

### LinkedIn

The backend uses LinkedIn 3-legged OAuth for member authorization and the current REST Posts API for text publishing when `w_member_social` is available to the application. LinkedIn's current API documentation states that Posts API replaces the older `ugcPosts` API and requires a version header plus `X-Restli-Protocol-Version: 2.0.0`.

### TikTok

Login Kit OAuth and the Content Posting API integration foundation are included. TikTok requires approved scopes/products for direct posting; unaudited clients can be restricted to private visibility.

### Meta

Meta Graph API client modules are included for Instagram, Facebook and WhatsApp. The exact Graph API version and product permissions must match the current Meta Developer configuration for the app.

### X

OAuth 2.0 + PKCE client and post creation client are included. Production deployments should use durable server-side state storage for PKCE/OAuth state.

## AI

AI provider abstraction supports OpenAI and Gemini through `app/integrations/ai/`. No API keys are hardcoded.

## ML

The baseline ML pipeline uses RandomForestRegressor. It refuses to train until there is enough historical data and refuses prediction until a trained model exists.

## Payments

Payment architecture supports M-Pesa, Airtel Money, Mixx by Yas, HaloPesa, cards and bank payments at the application layer. Provider-specific merchant APIs/webhooks must be configured with real credentials before production use. The backend does not fake payment verification.

## Tests

```bash
pytest -q
```

## Security

Never commit `.env`, Client Secrets, access tokens, refresh tokens, passwords, or private keys.

External API approval requirements are provider-controlled. The code includes integration boundaries and error handling but cannot grant API permissions that a provider has not granted to the developer application.
