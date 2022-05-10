from typing import Any
from fastapi import FastAPI

from api.config import init_config
from api.db.initialize import initialize_db
from api.routes.api import router as api_router


class DiscountManagerAPI(FastAPI):
    def __init__(self, **extra: Any):
        super().__init__(**extra)
        self.config = init_config()


app = DiscountManagerAPI()
app.include_router(api_router, prefix='/api')


@app.on_event("startup")
async def startup_event():
    await initialize_db(app.config.postgres)
