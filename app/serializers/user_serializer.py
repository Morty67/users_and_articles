from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str
    age: int = Field(..., gt=0, le=99)


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
