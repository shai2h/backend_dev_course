from fastapi import FastAPI
import uvicorn

from fastapi.openapi.docs import get_swagger_ui_html

# Добавляем корневую директорию проекта в sys.path, чтобы можно было использовать абсолютные импорты
# Это позволяет импортировать модули из src и других пакетов, несмотря на расположение запускаемого файла
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotel_router

from src.database import *

app = FastAPI()


app.include_router(hotel_router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,  # type: ignore
        title=app.title + " - Swagger UI",  # type: ignore
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,  # type: ignore
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)