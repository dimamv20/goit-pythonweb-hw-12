from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import contacts, auth, user
from database import engine, Base

app = FastAPI(title="Contacts API")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router)
app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
def home():
    return {"message": "Welcome to the Contacts API!"}
