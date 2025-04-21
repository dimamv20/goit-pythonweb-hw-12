from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis
import redis.asyncio as redis
from starlette.requests import Request

from app.database import Base, engine
from routers import auth, user, contacts
from config import settings

app = FastAPI(title="Контакти API з аутентифікацією, кешем та аватарами")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    app.state.redis = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
        encoding="utf-8",
        decode_responses=True
    )

@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()

@app.get("/")
def home():
    return {"message": "Вітаємо у REST API для контактів!"}

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
