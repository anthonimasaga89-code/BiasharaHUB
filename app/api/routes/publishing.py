from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.content import ContentResponse
from app.services.publishing_service import publish_content

router = APIRouter(prefix="/api/publishing", tags=["Publishing"])


@router.post("/{content_id}", response_model=ContentResponse)
async def publish(content_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return await publish_content(db, content_id, current_user.id)
