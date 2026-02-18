from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import pytz

from app.database import get_db   # ✅ FIX HERE
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter()

IST = pytz.timezone("Asia/Kolkata")


@router.post("/classes")
def create_class(
    class_data: schemas.ClassCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    class_time = class_data.dateTime.astimezone(IST)

    new_class = models.FitnessClass(
        name=class_data.name,
        date_time=class_time,
        instructor=class_data.instructor,
        available_slots=class_data.availableSlots
    )

    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return {
        "message": "Class created successfully",
        "class": {
            "id": new_class.id,
            "name": new_class.name,
            "dateTime": new_class.date_time,
            "instructor": new_class.instructor,
            "availableSlots": new_class.available_slots
        }
    }


@router.get("/classes")
def get_classes(db: Session = Depends(get_db)):
    classes = (
        db.query(models.FitnessClass)
        .filter(models.FitnessClass.date_time >= datetime.now(IST))
        .all()
    )

    return [
        {
            "id": c.id,
            "name": c.name,
            "dateTime": c.date_time,
            "instructor": c.instructor,
            "availableSlots": c.available_slots
        }
        for c in classes
    ]
