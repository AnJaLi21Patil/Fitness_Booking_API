from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.redis_client import redis_client
from app.database import SessionLocal
from app import models

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")


def handle_past_classes():
    # Redis lock
    lock = redis_client.setnx("past_class_job_lock", "1")
    if not lock:
        return

    redis_client.expire("past_class_job_lock", 120)

    db = SessionLocal()
    try:
        now = datetime.now()

        past_classes = (
            db.query(models.FitnessClass)
            .filter(models.FitnessClass.date_time < now)
            .all()
        )

        if past_classes:
            print(f"⏱ Found {len(past_classes)} past classes")

    except Exception as e:
        print("❌ Scheduler error:", e)

    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(
        handle_past_classes,
        trigger="interval",
        minutes=1,
        id="handle_past_classes",
        replace_existing=True,
    )
    scheduler.start()