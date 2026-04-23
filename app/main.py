from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import auth, admin_users, admin_roles, me, job_monitor
import app.db.base

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(me.router, prefix=f"{settings.API_V1_STR}/me", tags=["me"])
app.include_router(admin_users.router, prefix=f"{settings.API_V1_STR}/admin/users", tags=["admin_users"])
app.include_router(admin_roles.router, prefix=f"{settings.API_V1_STR}/admin/roles", tags=["admin_roles"])
app.include_router(job_monitor.router, prefix=f"{settings.API_V1_STR}/job-monitor", tags=["job_monitor"])

@app.get("/")
def root():
    return {"message": "Welcome to the Admin Auth System API. Go to /docs for Swagger UI."}
