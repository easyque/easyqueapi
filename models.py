from operator import index
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship
from databse import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    contact = Column(BigInteger)
    is_active = Column(Boolean, default=True)
    auth_token = Column(String)

