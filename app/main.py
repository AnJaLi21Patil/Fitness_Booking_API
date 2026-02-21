from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, classes, bookings
from app.scheduler import start_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Booking API")

app.include_router(users.router)
app.include_router(classes.router)
app.include_router(bookings.router)

@app.on_event("startup")
def startup_event():
    start_scheduler()