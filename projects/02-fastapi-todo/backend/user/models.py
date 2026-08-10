from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=False)
    password = Column(String)

    # make one to many relationship with todo
    todos = relationship("Todo", back_populates="user", cascade="all, delete")
