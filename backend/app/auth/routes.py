from fastapi import APIRouter, HTTPException, status, Request
from datetime import timedelta
from app.models import User
from app.schemas import UserCreate, UserLogin, Token, UserResponse
from app.auth.security import hash_password, verify_password, create_access_token
from app.auth.dependencies import get_current_active_user
from app.config import settings
from pymongo.errors import DuplicateKeyError
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user"""
    try:
        logger.info(f"🔔 Registration attempt - Email: {user_data.email}, Username: {user_data.username}")
        
        # Check if email already exists
        existing_user = await User.find_one(User.email == user_data.email)
        if existing_user:
            logger.warning(f"❌ Email already exists: {user_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username already exists
        existing_username = await User.find_one(User.username == user_data.username)
        if existing_username:
            logger.warning(f"❌ Username already taken: {user_data.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create new user
        hashed_pwd = hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_pwd
        )
        
        await new_user.insert()
        logger.info(f"✅ User registered successfully: {new_user.email} (ID: {new_user.id})")
        
        # Convert ObjectId to string for response
        user_response = UserResponse(
            id=str(new_user.id),
            email=new_user.email,
            username=new_user.username,
            is_active=new_user.is_active,
            created_at=new_user.created_at
        )
        
        return user_response
        
    except HTTPException:
        raise
    except DuplicateKeyError as e:
        logger.error(f"❌ Duplicate key error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already exists"
        )
    except Exception as e:
        logger.error(f"❌ Unexpected error during registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Login user and return JWT token"""
    try:
        logger.info(f"🔑 Login attempt for: {user_credentials.email}")
        
        # Find user by email
        user = await User.find_one(User.email == user_credentials.email)
        
        if not user:
            logger.warning(f"❌ User not found: {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not verify_password(user_credentials.password, user.hashed_password):
            logger.warning(f"❌ Wrong password for: {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            logger.warning(f"❌ Inactive account: {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        
        logger.info(f"✅ Successful login for: {user.email}")
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# from fastapi import APIRouter, Depends, HTTPException, status
# # from sqlalchemy.orm import Session
# from datetime import timedelta
# # from app.database import get_db
# from app.models import User
# from app.schemas import UserCreate, UserLogin, Token, UserResponse
# from app.auth.security import hash_password, verify_password, create_access_token
# from app.auth.dependencies import get_current_active_user
# from app.config import settings
# from pymongo.errors import DuplicateKeyError

# router = APIRouter(prefix="/auth", tags=["Authentication"])


# @router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# async def register(user_data: UserCreate):
# # async def register(user_data: UserCreate, db: Session = Depends(get_db)):
#     """
#     Register a new user
    
#     Args:
#         user_data: User registration data
        
#     Returns:
#         Created user information
        
#     Raises:
#         HTTPException: If email or username already exists
#     """
#     try:
#          # Check if email already exists
#         existing_user = await User.find_one(User.email == user_data.email)
#         if existing_user:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Email already registered"
#             )
        
#         # Check if username already exists
#         existing_username = await User.find_one(User.username == user_data.username)
#         if existing_username:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Username already taken"
#             )
        
#         # Create new user
#         hashed_pwd = hash_password(user_data.password)
#         new_user = User(
#             email=user_data.email,
#             username=user_data.username,
#             hashed_password=hashed_pwd
#         )
        
#         await new_user.insert()
#         return new_user
#         #mongodb


#         # Check if email already exists
#         # existing_user = db.query(User).filter(User.email == user_data.email).first()
#         # if existing_user:
#         #     raise HTTPException(
#         #         status_code=status.HTTP_400_BAD_REQUEST,
#         #         detail="Email already registered"
#         #     )

#         # # Check if username already exists
#         # existing_username = db.query(User).filter(User.username == user_data.username).first()
#         # if existing_username:
#         #     raise HTTPException(
#         #         status_code=status.HTTP_400_BAD_REQUEST,
#         #         detail="Username already taken"
#         #     )

#         # # Create new user
#         # hashed_pwd = hash_password(user_data.password)
#         # new_user = User(
#         #     email=user_data.email,
#         #     username=user_data.username,
#         #     hashed_password=hashed_pwd
#         # )

#         # db.add(new_user)
#         # db.commit()
#         # db.refresh(new_user)
#         # return new_user
    
#     except DuplicateKeyError:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email or username already exists"
#         )

# @router.post("/login", response_model=Token)
# async def login(user_credentials: UserLogin):
# # async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
#     """
#     Login user and return JWT token
    
#     Args:
#         user_credentials: User login credentials
        
#     Returns:
#         JWT access token
        
#     Raises:
#         HTTPException: If credentials are invalid
#     """
#     user = await User.find_one(User.email == user_credentials.email)
    
#     if not user or not verify_password(user_credentials.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Account is inactive"
#         )
    
#     # Create access token
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email},
#         expires_delta=access_token_expires
#     )
    
#     return {"access_token": access_token, "token_type": "bearer"}
#     #mongodb

#     # Find user by email
#     # user = db.query(User).filter(User.email == user_credentials.email).first()
    
#     # if not user or not verify_password(user_credentials.password, user.hashed_password):
#     #     raise HTTPException(
#     #         status_code=status.HTTP_401_UNAUTHORIZED,
#     #         detail="Incorrect email or password",
#     #         headers={"WWW-Authenticate": "Bearer"},
#     #     )
    
#     # if not user.is_active:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_403_FORBIDDEN,
#     #         detail="Account is inactive"
#     #     )
    
#     # # Create access token
#     # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     # access_token = create_access_token(
#     #     data={"sub": user.email},
#     #     expires_delta=access_token_expires
#     # )
    
#     # return {"access_token": access_token, "token_type": "bearer"}