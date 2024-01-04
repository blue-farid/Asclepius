from datetime import datetime
from pydantic import BaseModel

class ServerBase(BaseModel):
    ip: str

class ServerCreate(ServerBase):
    pass

class Server(ServerBase):
    id: int
    success: int
    failure: int
    last_failure: datetime
