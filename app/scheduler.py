from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
import redis
from app.database import SessionLocal
from app.models import FitnessClass

IST = pytz.timezone("Asia/Kolkata")

redis_client = redis.Redis(host="localhost", port=6379, db=0)

scheduler = BackgroundScheduler(timezone=IST)


def fetch_upcoming_classes():
    """Fetch upcoming classes and print in readable format"""
    db = SessionLocal()
    now = datetime.now(IST)
    upcoming = db.query(FitnessClass).filter(FitnessClass.date_time >= now).all()

    print("=== Upcoming Classes Check ===", now)
    if not upcoming:
        print("No upcoming classes found!")
    else:
        for cls in upcoming:
            print(
                f"ID: {cls.id}, Name: {cls.name}, Time: {cls.date_time}, "
                f"Instructor: {cls.instructor}, Slots: {cls.available_slots}"
            )

def fetch_past_classes():
    """Fetch past classes and print in readable format"""
    db = SessionLocal()
    now = datetime.now(IST)
    past = db.query(FitnessClass).filter(FitnessClass.date_time < now).all()

    print("=== Past Classes Check ===", now)
    if not past:
        print("No past classes found!")
    else:
        for cls in past:
            print(
                f"ID: {cls.id}, Name: {cls.name}, Time: {cls.date_time}, "
                f"Instructor: {cls.instructor}, Slots: {cls.available_slots}"
            )

def start_scheduler():
    """Call this from main.py to start the scheduler"""
    scheduler.add_job(fetch_upcoming_classes, 'interval', minutes=1)
    scheduler.add_job(fetch_past_classes, 'interval', minutes=1)
    scheduler.start()
    print("Scheduler started...")
    