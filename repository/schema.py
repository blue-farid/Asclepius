from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ServerBase(BaseModel):
    ip: str


class ServerCreate(ServerBase):
    pass


class Server(ServerBase):
    id: int
    success: Optional[int]
    failure: Optional[int]
    last_failure: Optional[datetime]

    class Config:
        from_attributes = True
