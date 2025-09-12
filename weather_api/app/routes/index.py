from fastapi import APIRouter, Request, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse

from weather_api import __version__
from weather_api.processors import app

router = APIRouter()


@router.get('/', include_in_schema=False)
def index(request: Request) -> RedirectResponse:
    return app.render_template('index.html', request=request)


@router.get('/openapi.json', include_in_schema=False)
def openapi():
    return JSONResponse(get_openapi(title='Weather API', version=__version__, routes=app.server.routes))


@router.get('/docs', include_in_schema=False)
def documentation():
    return get_swagger_ui_html(openapi_url=app.url_for('index.openapi'), title='docs')


@router.get('/healthcheck')
def healthcheck():
    return PlainTextResponse(content='It works', status_code=status.HTTP_200_OK)
