from fastapi import FastAPI 
from .notes import router
from .database import engine
from .models import Base
from fastapi.middleware.cors import CORSMiddleware


# async def lifespan(app: FastAPI)-> As
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins =origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
    
)


app.include_router(router , tags=['Notes'] , prefix='/api/notes')