from fastapi import FastAPI
from app.routers import oil_router
from app.tasks import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(oil_router)
