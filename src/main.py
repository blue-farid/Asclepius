from datetime import datetime
from typing import List
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from repository import crud, models, schema
from repository.database import SessionLocal, engine
from apscheduler.schedulers.background import BackgroundScheduler
from util import health_check_util

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/server/{id}")
async def get_server(id: int, db: Session = Depends(get_db), response_model=schema.Server):
    return crud.get_server(db, id)


@app.get("/api/server")
async def get_all_servers(db: Session = Depends(get_db), response_model=List[schema.Server]):
    return crud.get_all_servers(db)


@app.post("/api/server")
async def create_server(server: schema.ServerCreate, db: Session = Depends(get_db), response_model=schema.Server):
    return crud.create_server(db, server)


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()


def health_check_job():
    local_db = SessionLocal()
    try:
        print("Executing the scheduled job...")
        servers = crud.get_all_servers(local_db)
        for server in servers:
            server_schema = schema.Server.from_attributes(server)
            if not health_check_util.is_healthy(server_schema):
                server_schema.failure = server_schema.failure + 1
                server_schema.last_failure = datetime.utcnow()
            else:
                server_schema.success = server_schema.success + 1

            crud.update_server(local_db, server_schema)

        print("Job has finished!...")
    finally:
        local_db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(health_check_job, 'interval', seconds=10)
scheduler.start()
