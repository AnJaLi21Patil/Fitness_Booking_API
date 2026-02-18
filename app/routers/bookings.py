from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/book")
def book_class(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.User).filter(
        models.User.email == current_user
    ).first()

    fitness_class = db.query(models.FitnessClass).filter(
        models.FitnessClass.id == booking.class_id
    ).first()

    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found")

    if fitness_class.available_slots <= 0:
        raise HTTPException(status_code=400, detail="No slots available")

    new_booking = models.Booking(
        user_id=user.id,
        class_id=fitness_class.id,
        client_name=booking.client_name,
        client_email=booking.client_email
    )

    fitness_class.available_slots -= 1

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return {
        "message": "Booking successful",
        "booking_id": new_booking.id
    }


# ✅ NEW ENDPOINT
@router.get("/bookings")
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(models.User).filter(
        models.User.email == current_user
    ).first()

    bookings = (
        db.query(models.Booking, models.FitnessClass)
        .join(models.FitnessClass, models.Booking.class_id == models.FitnessClass.id)
        .filter(models.Booking.user_id == user.id)
        .all()
    )

    return [
        {
            "booking_id": booking.id,
            "class_name": fitness_class.name,
            "instructor": fitness_class.instructor,
            "dateTime": fitness_class.date_time
        }
        for booking, fitness_class in bookings
    ]
