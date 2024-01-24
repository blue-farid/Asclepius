from datetime import datetime
from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from repository import crud, models, schema
from repository.database import SessionLocal, engine
from util import health_check_util
from config import settings
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

scheduler = AsyncIOScheduler()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/server/{server_id}")
async def get_server(server_id: int, db: Session = Depends(get_db), response_model=schema.Server):
    return crud.get_server(db, server_id)


@app.get("/api/server")
async def get_all_servers(db: Session = Depends(get_db), response_model=List[schema.Server]):
    return crud.get_all_servers(db)


@app.post("/api/server")
async def create_server(server: schema.ServerCreate, db: Session = Depends(get_db), response_model=schema.Server):
    return crud.create_server(db, server)


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()


async def health_check_job():
    print("Executing the scheduled job...")
    db = SessionLocal()
    servers = crud.get_all_servers(db)
    for server in servers:
        server_schema = schema.Server(id=server.id, ip=server.ip, success=server.success, failure=server.failure,
                                      last_failure=server.last_failure)
        if not await health_check_util.is_healthy(server_schema):
            if server_schema.failure is not None:
                server_schema.failure = server_schema.failure + 1
            else:
                server_schema.failure = 1
            server_schema.last_failure = datetime.utcnow()
        else:
            if server_schema.success is not None:
                server_schema.success = server_schema.success + 1
            else:
                server_schema.success = 1

        crud.update_server(db, server_schema)
    print("Job has finished!...")

if __name__ == "__main__":
    uvicorn.run("asclepius:app", host="0.0.0.0", port=settings.app_port)

scheduler.add_job(health_check_job, 'interval', seconds=settings.health_check_time)
scheduler.start()
