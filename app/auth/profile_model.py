__all__ = ["Profile"]

from sqlalchemy import Column, Integer, String, Boolean

from app.core.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
