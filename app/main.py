from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="User Activity Tracker",
    description="A backend API for recording and querying user activity events",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1", tags=["events"])


@app.get("/")
def root():
    return {
        "message": "User Activity Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "OK"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
