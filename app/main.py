from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.routes import admin, analytics, auth, business, content, health, linkedin, meta, ml, orders, payments, products, publishing, social_accounts, tiktok, x_social, ai

app = FastAPI(title=settings.APP_NAME, version="1.0.0", debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError):
    messages = []
    for error in exc.errors():
        location = ".".join(str(part) for part in error.get("loc", ()) if part != "body")
        message = error.get("msg", "Invalid value")
        messages.append(f"{location}: {message}" if location else message)
    return JSONResponse(status_code=422, content={"detail": "; ".join(messages) or "Invalid request"})


uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

for router in [
    health.router,
    auth.router,
    business.router,
    products.router,
    social_accounts.router,
    linkedin.router,
    meta.router,
    tiktok.router,
    x_social.router,
    content.router,
    ai.router,
    publishing.router,
    orders.router,
    payments.router,
    analytics.router,
    ml.router,
    admin.router,
]:
    app.include_router(router)

frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
