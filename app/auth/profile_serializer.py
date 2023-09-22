from pydantic import BaseModel, EmailStr


class ProfileCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    hashed_password: str


class ProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    hashed_password: str
    disabled: bool
