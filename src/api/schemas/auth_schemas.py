from pydantic import BaseModel

class RegisterSchema(BaseModel):
    email: str
    username: str
    password: str

class LoginSchema(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str
