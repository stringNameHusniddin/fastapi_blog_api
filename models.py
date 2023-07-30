from database import Base 
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)

    username = Column(String)
    password = Column(String)
    email = Column(String)

    blogs = relationship("Blog", back_populates="owner")

class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    body = Column(String)
    url = Column(String)

    owner_id = Column(Integer, ForeignKey("user.id"))
    
    owner = relationship("User", back_populates="blogs")
