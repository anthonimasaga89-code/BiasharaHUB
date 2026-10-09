from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.content import AIGenerateRequest
from app.services.ai_service import adapt_content, generate_product_content
from app.services.content_service import get_content

router = APIRouter(prefix="/api/ai", tags=["AI"])


@router.post("/generate/business/{business_id}")
async def generate(business_id: int, data: AIGenerateRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return await generate_product_content(db, business_id, current_user.id, data)


@router.post("/adapt")
async def adapt(content_id: int, platform: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    content = get_content(db, content_id)
    from app.services.business_service import require_business_owner

    require_business_owner(db, content.business_id, current_user.id)
    return {"platform": platform, "content": await adapt_content(content.body, platform)}
