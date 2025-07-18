# routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from uuid import UUID

from ..database import get_session
from ..models import User
from ..schemas import UserLogin, UserRegister, Token, UserOut
from ..auth import verify_password, get_password_hash, create_access_token, get_current_active_user
from ..utils.email import send_email_async

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=201)
async def register_user(
    data: UserRegister,
    session: AsyncSession = Depends(get_session)
):
    """Register a new user and send a welcome email"""
    try:
        # Check if email already exists
        existing_user = await session.scalar(
            select(User).where(User.email == data.email)
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash the password
        hashed_password = get_password_hash(data.password)

        # Create user data without password
        user_data = data.dict()
        user_data.pop("password")
        user_data["password_hash"] = hashed_password

        new_user = User(**user_data)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        # Send welcome email (do not block registration if email fails)
        try:
            subject = "Welcome to CommunityPro Portal!"
            body = f"""
Hi {new_user.first_name},

Welcome to the CommunityPro Portal! Your account has been created successfully.

We will be in touch soon.

Best regards,
CommunityPro Team
"""
            await send_email_async(new_user.email, subject, body)
        except Exception as e:
            print(f"[WARN] Failed to send welcome email: {e}")

        return new_user
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to register user: {str(e)}")

@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    session: AsyncSession = Depends(get_session)
):
    """Login user and return access token"""
    try:
        # Find user by email
        user = await session.scalar(
            select(User).where(User.email == user_credentials.email)
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password
        if not verify_password(user_credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Update last login
        user.last_login_at = datetime.utcnow()
        await session.commit()
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role.value}
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.post("/login-form", response_model=Token)
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """Login using form data (for Swagger UI compatibility)"""
    try:
        # Find user by email
        user = await session.scalar(
            select(User).where(User.email == form_data.username)
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password
        if not verify_password(form_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        # Update last login
        user.last_login_at = datetime.utcnow()
        await session.commit()
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role.value}
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.get("/me", response_model=UserOut)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information"""
    return current_user

@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """Change user password"""
    try:
        # Verify current password
        if not verify_password(current_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect current password"
            )
        
        # Hash new password
        new_password_hash = get_password_hash(new_password)
        
        # Update password
        current_user.password_hash = new_password_hash
        current_user.updated_at = datetime.utcnow()
        
        await session.commit()
        
        return {"message": "Password changed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change password: {str(e)}"
        ) 