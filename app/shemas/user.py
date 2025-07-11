from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str
