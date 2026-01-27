import structlog
from fastapi import APIRouter

logger = structlog.get_logger()
router = APIRouter()


@router.get("/api/home")
async def home():
    logger.info("Home endpoint called")
    return {"message": "Hello, in Jabba pizza"}
