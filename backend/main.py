import logging
import sys
from contextlib import asynccontextmanager

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler
from database.mongo_client import is_empty
from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from routers import provider_router, user_router, account_router, backend_router, job_router, helper_router
from utils.scheduler_functions import init_backends, init_providers, job_manager, schedule_providers


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
        # No lo ejecuto en un hilo diferente para bloquear la ejecucion
        init_providers()
    # [x] REWORK: Si la coleccion de proveedores NO esta vacia, 
    # lanzar schedule semanal para actualizar los proveedores 
    # ('schedule_providers' se encarga de todo)
    else:
        logger.debug("Setting 'init_providers' function to run every week on Sunday at 0:00 AM")
        scheduler.add_job(
            func=schedule_providers,
            args=[scheduler],
            trigger="cron",
            minute="0",
            hour="0",
            day_of_week="sun",
            id="job_init_providers",
            replace_existing=True,
        )
        

    # Si la coleccion de backends esta vacia
    if is_empty("backends"):
        logger.debug("Setting 'init_backends' function to run immediately")
        scheduler.add_job(
            func=init_backends,
            args=[scheduler],
            id="job_init_backends",
            replace_existing=True,
        )
    # Si la coleccion de backends NO esta vacia
    else:
        logger.debug("Setting 'init_backends' function to run every day at 2:00 AM")
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

origins = [
    # docker
    "http://localhost",
    # develop
    "http://localhost:4200",
    # cloud
    "https://quantum-proxy.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    user_router.router,
    # prefix="/api/v1",
)

app.include_router(
    account_router.router,
    # prefix="/api/v1",
)

app.include_router(
    provider_router.router,
    # prefix="/api/v1",
)

app.include_router(
    backend_router.router,
    # prefix="/api/v1",
)

app.include_router(
    job_router.router,
    # prefix="/api/v1",
)

app.include_router(
    helper_router.router,
    # prefix="/api/v1",
)


@app.get("/")
async def root():
    return {"api_status": "Available!"}


@app.get("/health")
async def health():
    return {"status": "ok"}
