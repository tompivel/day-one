from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Training Logging App", version="0.1.0")

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:5173", # Vite default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import profiles, plans, macrocycles, microcycles, sessions, auth
from database import engine, Base

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(plans.router)
app.include_router(macrocycles.router)
app.include_router(microcycles.router)
app.include_router(sessions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Training Logging API"}
