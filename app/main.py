from fastapi import FastAPI
from app.api.routes import router
from app.db.database import Base, engine
from app.db import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Career Intelligence Agent",
    description="AI-powered assistant for job analysis and interview preparation.",
    version="0.1.0",
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
