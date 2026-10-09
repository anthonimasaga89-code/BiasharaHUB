from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.product import Product
from app.schemas.content import AIGenerateRequest
from app.services.business_service import require_business_owner
from app.integrations.ai import openai_provider, gemini_provider


def _provider():
    return openai_provider if settings.OPENAI_API_KEY else gemini_provider


async def generate_product_content(db: Session, business_id: int, user_id: int, data: AIGenerateRequest) -> dict:
    require_business_owner(db, business_id, user_id)
    product = db.query(Product).filter(Product.id == data.product_id, Product.business_id == business_id).first()
    if not product:
        raise HTTPException(404, "Product not found")
    prompt = f"""Create marketing content for this product.
Product: {product.name}
Description: {product.description or ''}
Price: {product.price}
Platform: {data.platform}
Language: {data.language}
Tone: {data.tone}
Goal: {data.goal}
Do not invent product facts. Include a clear call to action."""
    try:
        text = await _provider().generate_text(prompt)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc))
    return {"platform": data.platform, "content": text}


async def adapt_content(text: str, platform: str, language: str = "English") -> str:
    prompt = f"Adapt this marketing content for {platform}. Language: {language}. Preserve facts, price, and meaning. Content:\n{text}"
    try:
        return await _provider().generate_text(prompt)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc))
