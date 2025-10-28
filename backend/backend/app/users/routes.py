from fastapi import APIRouter, Depends
from app.models import User
from app.schemas import UserResponse
from app.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user information"""
    # Convert ObjectId to string for response
    user_response = UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )
    return user_response

# from fastapi import APIRouter, Depends
# from app.models import User
# from app.schemas import UserResponse
# from app.auth.dependencies import get_current_active_user

# router = APIRouter(prefix="/users", tags=["Users"])


# @router.get("/me", response_model=UserResponse)
# async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
#     """
#     Get current authenticated user information
    
#     Args:
#         current_user: Current authenticated user from JWT token
        
#     Returns:
#         Current user information
#     """
#     return current_user