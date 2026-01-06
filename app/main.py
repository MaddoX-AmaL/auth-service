from fastapi import FastAPI
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])

class UserCreate(BaseModel):
    email: str
    password: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/signup")
def signup(user: UserCreate):
    hashed_password = hash_password(user.password)
    return {
        "email": user.email,
        "hashed_password": hashed_password
    }
