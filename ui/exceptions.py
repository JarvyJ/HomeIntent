from typing import Any, Dict, Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class HomeIntentHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        title: str,
        detail: Any = None,
        links_about: str = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.title = title
        self.links_about = links_about


async def http_exception_handler(request: Request, exc: HomeIntentHTTPException) -> JSONResponse:
    error_object = {"title": exc.title, "detail": exc.detail, "status_code": f"{exc.status_code}"}
    if exc.links_about:
        error_object["links"] = {"about": exc.links_about}

    if exc.headers:
        return JSONResponse(error_object, status_code=exc.status_code, headers=exc.headers)
    else:
        return JSONResponse(error_object, status_code=exc.status_code)
