import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.database import init_db
from routers import auth, finance

LOCAL_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://[::1]:5173",
]


def get_allowed_origins() -> list[str]:
    frontend_url = os.getenv("FRONTEND_URL", "").strip()
    extra = [frontend_url] if frontend_url else []
    return LOCAL_ORIGINS + extra


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="MyWallet API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(finance.router, prefix="/finance", tags=["Finance"])


@app.get("/health")
def health():
    return {"status": "ok"}
