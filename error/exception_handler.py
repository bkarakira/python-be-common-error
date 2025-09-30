from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    code: str
    message: str
    status_code: int
    details: dict

    def __init__(self, code: str, message: str, status_code: int = 400, details: dict = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)

def register_exception_handlers(app: FastAPI, logger = None):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        if logger:
            logger.error(f"AppException: {exc.code} - {exc.message}")
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
