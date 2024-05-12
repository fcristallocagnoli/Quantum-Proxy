import logging
import sys
from contextlib import asynccontextmanager

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler
from database.mongo_client import is_empty
from fastapi import FastAPI
from fastapi.logger import logger
from routers import auth_router, provider_router, user_router
from utils.scheduler_functions import init_backends, init_providers, job_manager


def init_logger():
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    log_formatter = logging.Formatter(
        "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
    )
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)


def init_database(scheduler: BackgroundScheduler):
    # Si la coleccion de proveedores esta vacia
    if is_empty("providers"):
        logger.debug("Initializing providers")
        init_providers()
    # Si la coleccion de backends esta vacia
    if is_empty("backends"):
        logger.debug("Calling init_backends function (in first run)")
        scheduler.add_job(
            func=init_backends,
            args=[scheduler],
            id="job_init_backends",
            replace_existing=True,
        )
    # Si la coleccion de backends NO esta vacia
    else:
        logger.debug("Calling init_backends function (scheduled) every day at 2:00 AM")
        scheduler.add_job(
            func=init_backends,
            args=[scheduler],
            trigger="cron",
            minute="0",
            hour="2",
            id="job_init_backends",
            replace_existing=True,
        )


def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_listener(job_manager, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    return scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializar el logger
    init_logger()
    # ---------------------
    # Inicializar el scheduler
    scheduler = init_scheduler()
    init_database(scheduler)
    # ---------------------
    logger.debug("Starting scheduler")
    logger.debug(f"Jobs queued: {scheduler.get_jobs()}")
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


app.include_router(
    auth_router.router,
)

app.include_router(
    user_router.router,
)

app.include_router(
    provider_router.router,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "ok"}
