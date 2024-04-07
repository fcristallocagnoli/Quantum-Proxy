from fastapi import FastAPI
from routers import provider_router

app = FastAPI(
    title="Quantum Proxy API",
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
