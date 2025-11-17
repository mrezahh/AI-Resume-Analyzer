from fastapi import FastAPI
from database import engine, Base
from routers import auth

# Create the database tables
Base.metadata.create_all(bind=engine) 

app = FastAPI(title="Resume AI Analyzer")

app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Resume AI Analyzer API"}