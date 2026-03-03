# app/main.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import get_settings

from app.routers.router import api_router
from app.core.logging import setup_logging

settings = get_settings()

# Setup logging before creating the app
setup_logging()

app = FastAPI(
    title="Case Data Engineer API",
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
    swagger_css_url="https://cdn.jsdelivr.net/gh/Itz-fork/Fastapi-Swagger-UI-Dark/assets/swagger_ui_dark.min.css"
)

app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
