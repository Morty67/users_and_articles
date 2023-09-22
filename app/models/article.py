__all__ = ["Article"]

from enum import Enum

from sqlalchemy import Column, Integer, String, Enum as EnumType, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)

    class ColorEnum(str, Enum):
        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    color = Column(EnumType(ColorEnum), index=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="articles")
