from fastapi import FastAPI
from routers import items,users
import models
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(items.router)
app.include_router(users.router)
