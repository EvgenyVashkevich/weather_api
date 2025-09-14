import logging

from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from weather_api.processors import app

Exceptions = HTTPException | type[Exception] | Exception | RequestValidationError
_logger = logging.getLogger(__name__)


class ErrorResponse(BaseModel):
    error: str


def handle_exception(status_code: int, message: str) -> JSONResponse:
    """Return formatted response for received exception"""

    return JSONResponse(content=dict(error=message), status_code=status_code)


@app.server.exception_handler(RequestValidationError)
def validation(_: Request, exc: Exceptions):
    return handle_exception(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message=exc.detail,  # type: ignore[union-attr]
    )


@app.server.exception_handler(Exception)
def system(_: Request, exc: Exceptions):
    _logger.error(exc)
    return handle_exception(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal server error"
    )


@app.server.exception_handler(HTTPException)
def http(_: Request, exc: Exceptions):
    _logger.debug(exc)
    return handle_exception(status_code=exc.status_code, message=exc.detail)  # type: ignore[union-attr]
