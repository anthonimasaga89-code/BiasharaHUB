from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.content import Content
from app.models.social_account import SocialAccount
from app.services.business_service import require_business_owner
from app.integrations.social.linkedin.client import create_text_post
from app.integrations.social.x.client import create_post as x_create_post


async def publish_content(db: Session, content_id: int, user_id: int):
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(404, "Content not found")
    require_business_owner(db, content.business_id, user_id)
    if not content.platform:
        raise HTTPException(400, "Content platform is required")
    account = db.query(SocialAccount).filter(
        SocialAccount.business_id == content.business_id,
        SocialAccount.platform == content.platform.lower(),
        SocialAccount.is_connected.is_(True),
    ).first()
    if not account:
        raise HTTPException(404, "Connected social account not found")

    try:
        if account.platform == "linkedin":
            post_id = await create_text_post(account.access_token, account.account_id, content.body)
        elif account.platform == "x":
            result = await x_create_post(account.access_token, content.body)
            post_id = result.get("data", {}).get("id", "")
        else:
            raise HTTPException(501, f"Publishing adapter for {account.platform} requires provider-specific media flow")
    except HTTPException:
        raise
    except Exception as exc:
        content.status = "FAILED"
        content.failure_reason = str(exc)[:1000]
        db.commit()
        raise HTTPException(502, "Social provider rejected the publishing request")

    content.status = "PUBLISHED"
    content.provider_post_id = post_id
    content.failure_reason = None
    db.commit()
    db.refresh(content)
    return content
