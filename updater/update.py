from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .reservation_track import reservation_track

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(reservation_track, 'interval', seconds=20)
    scheduler.start()
