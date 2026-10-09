from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, decode_token, hash_password, verify_password
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, UserRole

ALLOWED_ROLES = {role.value for role in UserRole}


def register_user(db: Session, data: RegisterRequest):
    if data.role not in ALLOWED_ROLES:
        raise HTTPException(400, "Invalid role")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(409, "Email already registered")
    if data.phone and db.query(User).filter(User.phone == data.phone).first():
        raise HTTPException(409, "Phone already registered")
    user = User(
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        password_hash=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, data: LoginRequest):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    if not user.is_active:
        raise HTTPException(403, "User account is inactive")
    access = create_access_token(user.id, user.role)
    refresh, expires = create_refresh_token(user.id)
    db.add(RefreshToken(user_id=user.id, token=refresh, expires_at=expires.replace(tzinfo=None)))
    db.commit()
    return access, refresh


def refresh_access_token(db: Session, token: str):
    try:
        payload = decode_token(token)
        if payload.get("type") != "refresh":
            raise ValueError
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(401, "Invalid or expired refresh token")
    stored = db.query(RefreshToken).filter(RefreshToken.token == token, RefreshToken.revoked.is_(False)).first()
    if not stored or stored.expires_at <= datetime.utcnow():
        raise HTTPException(401, "Refresh token is invalid or expired")
    user = db.query(User).filter(User.id == user_id, User.is_active.is_(True)).first()
    if not user:
        raise HTTPException(401, "User not found")
    return create_access_token(user.id, user.role)


def logout_user(db: Session, token: str):
    stored = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if stored:
        stored.revoked = True
        db.commit()
