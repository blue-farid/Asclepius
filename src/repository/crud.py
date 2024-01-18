from .models import Server
from sqlalchemy.orm import Session
from .schema import ServerCreate
from .schema import Server as schema_server


def get_server(db: Session, server_id: int):
    return db.query(Server).filter(Server.id == server_id).first()


def get_all_servers(db: Session):
    return db.query(Server).all()


def create_server(db: Session, server: ServerCreate):
    db_server = Server(ip=server.ip)
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server


def update_server(db: Session, server: schema_server):
    db_server = Server(id=server.id, last_failure=server.last_failure, success=server.success, failure=server.failure)

    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server
