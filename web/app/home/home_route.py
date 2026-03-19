import structlog
from fastapi import APIRouter, Response

logger = structlog.get_logger()
router = APIRouter()


@router.get("/api/home")
async def home(response: Response):
    response.headers["Cache-Control"] = "no-store"

    logger.info("Home endpoint called")
    return {"message": "Hello, in Jabba pizza"}
