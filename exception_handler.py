import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from common_backend.logger.logging import get_logger


class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, details: dict = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details

def register_exception_handlers(app: FastAPI, logger: logging.Logger = None):
    logger = logger or get_logger("common_backend")
    @app.exception_handler(AppException)
    async def app_exception_handler(exc: AppException, request: Request):
        logger.error(f"{exc.code}: {exc.message} - {exc.details}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )
