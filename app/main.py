from fastapi import FastAPI
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ---------- PASSWORD UTILS ----------

def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)

# ---------- SCHEMAS ----------

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# ---------- FAKE DATABASE ----------

fake_user_db = {
    "email": "test@gmail.com",
    "hashed_password": hash_password("123456")
}

# ---------- ROUTES ----------

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

@app.post("/login")
def login(user: UserLogin):
    if user.email != fake_user_db["email"]:
        return {"message": "User not found"}

    if not verify_password(user.password, fake_user_db["hashed_password"]):
        return {"message": "Invalid password"}

    return {"message": "Login successful"}
