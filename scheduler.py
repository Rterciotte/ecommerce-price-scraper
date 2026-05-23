from apscheduler.schedulers.blocking import (
    BlockingScheduler
)

from src.jobs.scheduled_scraper import (
    run_scheduled_scraping
)


# ======================================
# SCHEDULER
# ======================================

scheduler = BlockingScheduler()


# ======================================
# RUN EVERY 1 MINUTE
# ======================================

scheduler.add_job(

    run_scheduled_scraping,

    "interval",

    minutes=1
)


print(
    "Scheduler started..."
)

scheduler.start()