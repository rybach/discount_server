from fastapi import APIRouter

from . import discount

router = APIRouter()
router.include_router(discount.router, tags=['discount'])
