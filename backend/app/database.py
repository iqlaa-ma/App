# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

from motor.motor_asyncio import AsyncIOMotorClient#mongodb
from beanie import init_beanie #mongodb
# from app.models import User #mongodb

from app.config import settings

#mongodb
# Global MongoDB client
mongodb_client: AsyncIOMotorClient = None


async def connect_to_mongo():
    """Create database connection"""
    global mongodb_client
    from app.models import User
    mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    # Initialize Beanie with the User model
    await init_beanie(
        database=mongodb_client[settings.DATABASE_NAME],
        document_models=[User]
    )


async def close_mongo_connection():
    """Close database connection"""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()


def get_database():
    """Get database instance"""
    return mongodb_client[settings.DATABASE_NAME]
#mongodb

# Create database engine
# engine = create_engine(
#     settings.DATABASE_URL,
#     connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
# )

# # Create session factory
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class for models
# Base = declarative_base()


# def get_db():
#     """Dependency to get database session"""
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# def init_db():
#     """Initialize database tables"""
#     Base.metadata.create_all(bind=engine)