from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from repository import crud, models, schema
from repository.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/server/{id}")
async def get_server(id: int, db: Session = Depends(get_db)):
    return crud.get_server(db, id)

@app.get("/api/server/all")
async def get_all_servers(db: Session = Depends(get_db)):
    return crud.get_all_servers(db)

@app.post("/api/server")
async def create_server(server: schema.ServerCreate, db: Session = Depends(get_db)):
    return crud.create_server(db, server)


