from datetime import datetime
from .database import Base
from sqlalchemy import Column, Integer, String, DateTime

class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, unique=True ,index=True)
    success = Column(Integer)
    failure = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_failure = Column(DateTime)
