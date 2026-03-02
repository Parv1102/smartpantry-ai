from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base

from routes.recipes import router as recipe_router


# Create tables
Base.metadata.create_all(bind=engine)

# Create app 
app = FastAPI(title="Smart Pantry AI API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(recipe_router)


@app.get("/")
def root():
    return {"message": "Smart Pantry AI running"}