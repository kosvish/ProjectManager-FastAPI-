from fastapi import FastAPI
from src.auth.router import router as user_router

app = FastAPI(title="GitHub")

app.include_router(user_router)
