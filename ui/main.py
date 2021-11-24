from exceptions import HomeIntentHTTPException, http_exception_handler
from pathlib import Path

from fastapi import FastAPI, Request
from pydantic import ValidationError
from starlette.staticfiles import StaticFiles
import uvicorn

from routers import rhasspy, settings, websockets

app = FastAPI(
    docs_url="/openapi",
    title="Home Intent UI",
    description="A simple web interface to help manage Home Intent. NOTE: This API should be considered unstable",
    version="2021.10.0b1",
)


@app.exception_handler(HomeIntentHTTPException)
async def home_intent_http_exception_handler(request, exc):
    return await http_exception_handler(request, exc)


# displays any errors the user may have put into the config.yaml file manually
@app.exception_handler(ValidationError)
async def yaml_config_validation_handler(request: Request, exc: ValidationError):
    error_message = "; ".join(str(exc).split("\n")[1:])
    home_intent_exception = HomeIntentHTTPException(
        400, title=f"Validation error in /config/config.yaml: {error_message}", detail=exc.errors()
    )
    return await http_exception_handler(request, home_intent_exception)


app.include_router(settings.router, prefix="/api/v1", tags=["Settings"])
app.include_router(rhasspy.router, prefix="/api/v1", tags=["Rhasspy Audio"])
app.include_router(websockets.router, tags=["Websocket Things"])

built_docs_dir = Path(__file__).parent.resolve().parent / "docs/site"
if built_docs_dir.exists():
    app.mount(
        "/docs/", StaticFiles(directory=built_docs_dir, html=True), name="documentation",
    )
else:
    print("The docs directory must exist (mkdocs build) for the documentation link to work")

built_frontend_dir = Path(__file__).parent.resolve() / "frontend/build"
if built_frontend_dir.exists():
    app.mount(
        "/",
        StaticFiles(directory=built_frontend_dir, html=True),
        name="frontend",
    )
else:
    print("Frontend must be built (npm run build) to be properly loaded. Will continue with just API: http://localhost:11102/openapi")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=11102, log_level="info", reload=True)
