# routes/users.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from ..database import get_session
from ..models import User
from ..schemas import UserCreate, UserUpdate, UserOut, UserApproval
from ..auth import get_current_active_user, require_role, require_roles, get_password_hash, create_access_token
from datetime import timedelta
from ..utils.email import send_email_async

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut, status_code=201)
async def create_user(
    data: UserCreate, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles(["super_admin", "property_manager"]))
):
    """Create a new user (Admin only)"""
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
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create user: {str(e)}")

@router.get("/", response_model=List[UserOut])
async def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    role: Optional[str] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    email_verified: Optional[bool] = Query(None, description="Filter by email verification status"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles(["super_admin", "property_manager", "board_member"]))
):
    """Get all users with optional filtering and pagination"""
    try:
        query = select(User)
        
        if role:
            # Import UserRole enum to validate the role parameter
            from ..models import UserRole
            
            # Validate that the role is a valid enum value
            try:
                user_role = UserRole(role)
                query = query.where(User.role == user_role)
            except ValueError:
                valid_roles = [r.value for r in UserRole]
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid role. Valid roles are: {', '.join(valid_roles)}"
                )
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        if email_verified is not None:
            query = query.where(User.email_verified == email_verified)
        if search:
            query = query.where(
                (User.first_name.ilike(f"%{search}%")) |
                (User.last_name.ilike(f"%{search}%")) |
                (User.email.ilike(f"%{search}%"))
            )
        
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: UUID, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific user by ID"""
    try:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user: {str(e)}")

@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: UUID, 
    updates: UserUpdate, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Update a user"""
    try:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        update_data = updates.dict(exclude_unset=True)
        
        # Check if email is being updated and if it already exists
        if 'email' in update_data and update_data['email'] != user.email:
            existing_user = await session.scalar(
                select(User).where(User.email == update_data['email'])
            )
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")
        
        for key, value in update_data.items():
            setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(user)
        return user
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update user: {str(e)}")

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles(["super_admin", "property_manager"]))
):
    """Delete a user"""
    try:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await session.delete(user)
        await session.commit()
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete user: {str(e)}")

@router.get("/email/{email}", response_model=UserOut)
async def get_user_by_email(
    email: str, 
    session: AsyncSession = Depends(get_session)
):
    """Get a user by email address"""
    try:
        user = await session.scalar(select(User).where(User.email == email))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user: {str(e)}")

@router.get("/role/{role}", response_model=List[UserOut])
async def get_users_by_role(
    role: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    session: AsyncSession = Depends(get_session)
):
    """Get all users with a specific role"""
    try:
        # Import UserRole enum to validate the role parameter
        from ..models import UserRole
        
        # Validate that the role is a valid enum value
        try:
            user_role = UserRole(role)
        except ValueError:
            valid_roles = [r.value for r in UserRole]
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid role. Valid roles are: {', '.join(valid_roles)}"
            )
        
        query = select(User).where(User.role == user_role).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

@router.put("/{user_id}/verify-email", response_model=UserOut)
async def verify_user_email(
    user_id: UUID, 
    session: AsyncSession = Depends(get_session)
):
    """Mark a user's email as verified"""
    try:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.email_verified = True
        user.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(user)
        return user
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to verify email: {str(e)}")

@router.put("/{user_id}/activate", response_model=UserOut)
async def activate_user(
    user_id: UUID, 
    session: AsyncSession = Depends(get_session)
):
    """Activate a user account"""
    try:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.is_active = True
        user.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(user)
        return user
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to activate user: {str(e)}")

@router.put("/{user_id}/deactivate", response_model=UserOut)
async def deactivate_user(
    user_id: UUID, 
    session: AsyncSession = Depends(get_session)
):
    """Deactivate a user account"""
    try:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(user)
        return user
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to deactivate user: {str(e)}")

@router.post("/approve", status_code=200)
async def approve_user(
    data: UserApproval,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role("super_admin"))
):
    """Approve a pending user, assign a role, and send password setup email"""
    from ..models import UserRole
    try:
        user = await session.get(User, data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_active:
            raise HTTPException(status_code=400, detail="User is already active")
        if data.role not in [r.value for r in UserRole if r.value in ("board_member", "community_admin", "property_manager")]:
            raise HTTPException(status_code=400, detail="Invalid role for approval")
        # Assign role and set as inactive until password is set
        user.role = UserRole(data.role)
        user.is_active = False
        # Generate password setup token (valid for 24h)
        expires = datetime.utcnow() + timedelta(hours=24)
        token_data = {"sub": str(user.id), "email": user.email, "purpose": "setup_password"}
        token = create_access_token(token_data, expires_delta=timedelta(hours=24))
        user.password_reset_token = token
        user.password_reset_expires = expires
        await session.commit()
        # Send setup password email
        try:
            link = f"http://localhost:8000/setup-password?token={token}"
            subject = "Your CommunityPro Account is Approved - Set Your Password"
            body = f"""
Hi {user.first_name},

Your account has been approved! Please set your password using the link below:

{link}

This link will expire in 24 hours.

Best regards,
CommunityPro Team
"""
            await send_email_async(user.email, subject, body)
        except Exception as e:
            print(f"[WARN] Failed to send setup password email: {e}")
        return {"message": "User approved and setup email sent."}
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to approve user: {str(e)}")

@router.get("/stats/summary", response_model=dict)
async def get_user_summary(
    session: AsyncSession = Depends(get_session)
):
    """Get user summary statistics"""
    try:
        # Get total count
        total_count = await session.scalar(select(func.count(User.id)))
        
        # Get active count
        active_count = await session.scalar(select(func.count(User.id)).where(User.is_active == True))
        
        # Get verified email count
        verified_count = await session.scalar(select(func.count(User.id)).where(User.email_verified == True))
        
        # Get counts by role
        role_counts = {}
        roles = ['super_admin', 'property_manager', 'board_member', 'community_admin', 'resident', 'tenant']
        
        for role in roles:
            count = await session.scalar(select(func.count(User.id)).where(User.role == role))
            role_counts[role] = count or 0
        
        return {
            "total_users": total_count or 0,
            "active_users": active_count or 0,
            "verified_emails": verified_count or 0,
            "inactive_users": (total_count or 0) - (active_count or 0),
            "unverified_emails": (total_count or 0) - (verified_count or 0),
            "role_distribution": role_counts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user summary: {str(e)}")

@router.get("/{user_id}/residents", response_model=dict)
async def get_user_residents(
    user_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    """Get all residents associated with a user"""
    try:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "user_id": user_id,
            "user_name": f"{user.first_name} {user.last_name}",
            "residents_count": len(user.residents) if user.residents else 0,
            "residents": user.residents
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user residents: {str(e)}") 