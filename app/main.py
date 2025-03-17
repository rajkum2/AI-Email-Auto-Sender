from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import lead_qualification
from config.config import get_settings

settings = get_settings()

app = FastAPI(
    title="AI Email Auto Sender",
    description="An AI-powered system for automatic email processing and lead qualification",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    lead_qualification.router,
    prefix=f"{settings.API_V1_PREFIX}/leads",
    tags=["leads"]
)

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "AI Email Auto Sender",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    ) 