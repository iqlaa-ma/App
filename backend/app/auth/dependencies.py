# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models import User
# from app.auth.security import decode_access_token
# from typing import Optional

# # Security scheme for JWT bearer token
# security = HTTPBearer()


# async def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
#     db: Session = Depends(get_db)
# ) -> User:
#     """
#     Dependency to get current authenticated user from JWT token
    
#     Args:
#         credentials: JWT token from Authorization header
#         db: Database session
        
#     Returns:
#         Current authenticated user
        
#     Raises:
#         HTTPException: If token is invalid or user not found
#     """
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
    
#     token = credentials.credentials
#     payload = decode_access_token(token)
    
#     if payload is None:
#         raise credentials_exception
    
#     email: Optional[str] = payload.get("sub")
#     if email is None:
#         raise credentials_exception
    
#     user = db.query(User).filter(User.email == email).first()
#     if user is None:
#         raise credentials_exception
    
#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Inactive user"
#         )
    
#     return user


# async def get_current_active_user(
#     current_user: User = Depends(get_current_user)
# ) -> User:
#     """
#     Dependency to ensure user is active
    
#     Args:
#         current_user: Current authenticated user
        
#     Returns:
#         Active user
        
#     Raises:
#         HTTPException: If user is inactive
#     """
#     if not current_user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Inactive user"
#         )
#     return current_user

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models import User
from app.auth.security import decode_access_token
from typing import Optional

# Security scheme for JWT bearer token
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Dependency to get current authenticated user from JWT token
    
    Args:
        credentials: JWT token from Authorization header
        
    Returns:
        Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
    
    email: Optional[str] = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = await User.find_one(User.email == email)
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure user is active
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Active user
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user