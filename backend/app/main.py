from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import (
    users_router,
    auth_router,
    accounts_router,
    inputs_router,
    health_router,
    dashboard_router,
    contracts_router,
    alerts_router,
    reminders_router,
    llm_settings_router
)
from contextlib import asynccontextmanager
from app.core.scheduler import start_scheduler, scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(accounts_router, prefix=f"{settings.API_V1_STR}/accounts", tags=["accounts"])
app.include_router(inputs_router, prefix=f"{settings.API_V1_STR}/inputs", tags=["inputs"])
app.include_router(llm_settings_router, prefix=f"{settings.API_V1_STR}/settings/llm", tags=["settings"])
app.include_router(health_router, prefix=f"{settings.API_V1_STR}/health", tags=["health"])
app.include_router(dashboard_router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["dashboard"])
app.include_router(contracts_router, prefix=f"{settings.API_V1_STR}/contracts", tags=["contracts"])
app.include_router(alerts_router, prefix=f"{settings.API_V1_STR}/alerts", tags=["alerts"]) # Using root prefix for nested routes consistency
app.include_router(reminders_router, prefix=f"{settings.API_V1_STR}/reminders", tags=["reminders"])

@app.get("/")
def read_root():
    return {"message": "Customer Pulse API"}
