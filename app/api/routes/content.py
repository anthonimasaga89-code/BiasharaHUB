from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.content import ContentCreate, ContentResponse
from app.services.content_service import create_content, get_content, list_business_content

router = APIRouter(prefix="/api/content", tags=["Content"])


@router.post("/business/{business_id}", response_model=ContentResponse, status_code=201)
def create(business_id: int, data: ContentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_content(db, business_id, data, current_user.id)


@router.get("/business/{business_id}", response_model=list[ContentResponse])
def list_content(business_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return list_business_content(db, business_id, current_user.id)


@router.get("/{content_id}", response_model=ContentResponse)
def get_one(content_id: int, db: Session = Depends(get_db)):
    return get_content(db, content_id)
