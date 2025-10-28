# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.database import init_db
# from app.auth.routes import router as auth_router
# from app.users.routes import router as users_router
# from app.config import settings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import connect_to_mongo, close_mongo_connection
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready authentication API for mobile apps",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This should allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)


# @app.on_event("startup")
# async def startup_event():
#     """Initialize database on startup"""
#     init_db()

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    try:
        await connect_to_mongo()
        print("✅ MongoDB connected successfully!")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await close_mongo_connection()
    print("✅ MongoDB connection closed")

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "database": "MongoDB" #mongodb 
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        # "database": "connected"
        "database": "MongoDB connected" #mongodb
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )