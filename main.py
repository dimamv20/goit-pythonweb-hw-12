from fastapi import FastAPI
from database import engine, Base
from routers import contacts

app = FastAPI(title="Контакти API")

Base.metadata.create_all(bind=engine)

app.include_router(contacts.router)

@app.get("/")
def home():
    return {"message": "Вітаю! Це API для контактів."}
