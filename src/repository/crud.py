from .models import Server
from sqlalchemy.orm import Session
from .schema import ServerCreate

def get_server(db: Session, id: int):
    return db.query(Server).filter(Server.id == id).first()

def get_all_servers(db: Session):
    return db.query(Server).all()

def create_server(db: Session, server: ServerCreate):
    db_server = Server(ip=server.ip)
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server


