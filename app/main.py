from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, classes, bookings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Booking API")

app.include_router(users.router)
app.include_router(classes.router)
app.include_router(bookings.router)
