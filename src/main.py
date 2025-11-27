from fastapi import FastAPI
import uvicorn

# Добавляем корневую директорию проекта в sys.path, чтобы можно было использовать абсолютные импорты
# Это позволяет импортировать модули из src и других пакетов, несмотря на расположение запускаемого файла
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotel_router

from src.config import settings


app = FastAPI()


app.include_router(hotel_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)