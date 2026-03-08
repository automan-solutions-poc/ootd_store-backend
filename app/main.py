from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.api.v1.auth import router as auth_router
from app.api.v1.admin.products import router as admin_products_router
from app.api.v1.admin.orders import router as admin_orders_router
from app.api.v1.admin.users import router as admin_users_router
from app.api.v1.admin.analytics import router as admin_analytics_router
from app.api.v1.customer.products import router as customer_products_router
from app.api.v1.customer.orders import router as customer_orders_router
from app.utils.exceptions import AppException
from fastapi.responses import JSONResponse

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Logging Middleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            "request_processed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration=f"{process_time:.4f}s"
        )
        return response

app.add_middleware(LoggingMiddleware)

# Exception Handling
@app.exception_handler(AppException)
async def app_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error("unhandled_exception", error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Routers
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

# Admin
app.include_router(admin_products_router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin-products"])
app.include_router(admin_orders_router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin-orders"])
app.include_router(admin_users_router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin-users"])
app.include_router(admin_analytics_router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin-analytics"])

# Customer
app.include_router(customer_products_router, prefix=f"{settings.API_V1_STR}/customer", tags=["customer-products"])
app.include_router(customer_orders_router, prefix=f"{settings.API_V1_STR}/customer", tags=["customer-orders"])

@app.get("/")
async def root():
    return {"message": "Welcome to Clothing E-commerce API"}
