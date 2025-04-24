from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Database
from app.utils.template_manager import TemplateManager
from app.services.email_service import EmailService
from app.services.jwt_service import decode_token
from settings.config import Settings

# App settings provider
def get_settings() -> Settings:
    return Settings()

# Email service provider
def get_email_service() -> EmailService:
    template_manager = TemplateManager()
    return EmailService(template_manager=template_manager)

# Database session dependency
async def get_db() -> AsyncSession:
    async_session_factory = Database.get_session_factory()
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Bearer token scheme for authentication
bearer_scheme = HTTPBearer()

# Authenticated user resolver
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id: str = payload.get("sub")
    user_role: str = payload.get("role")

    if user_id is None or user_role is None:
        raise HTTPException(status_code=401, detail="Invalid token claims")

    return {"user_id": user_id, "role": user_role}

# Role-based access control dependency
def require_role(roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return current_user
    return role_checker
