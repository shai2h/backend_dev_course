from fastapi import Query, Body, APIRouter, HTTPException
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep


router = APIRouter()


hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Москва", "name": "moskva"},
    {"id": 4, "title": "Казань", "name": "kazan"},
    {"id": 5, "title": "Санкт-Петербург", "name": "sankt-peterburg"},
    {"id": 6, "title": "Новосибирск", "name": "novosibirsk"},
    {"id": 7, "title": "Екатеринбург", "name": "ekaterinburg"},
    {"id": 8, "title": "Тбилиси", "name": "tbilisi"},
    {"id": 9, "title": "Баку", "name": "baku"},
    {"id": 10, "title": "Алушта", "name": "alushta"},
    {"id": 11, "title": "Геленджик", "name": "gelenjik"},
    {"id": 12, "title": "Анапа", "name": "anapa"},
    {"id": 13, "title": "Владивосток", "name": "vladivostok"},
    {"id": 14, "title": "Калининград", "name": "kaliningrad"},
    {"id": 15, "title": "Симферополь", "name": "simferopol"},
    {"id": 16, "title": "Уфа", "name": "ufa"},
    {"id": 17, "title": "Челябинск", "name": "chelyabinsk"},
    {"id": 18, "title": "Ростов-на-Дону", "name": "rostov-na-donu"},
    {"id": 19, "title": "Краснодар", "name": "krasnodar"},
    {"id": 20, "title": "Минеральные Воды", "name": "mineralnye-vody"},
    {"id": 21, "title": "Прага", "name": "praga"},
    {"id": 22, "title": "Берлин", "name": "berlin"},
    {"id": 23, "title": "Стамбул", "name": "stambul"},
    {"id": 24, "title": "Бангкок", "name": "bangkok"},
    {"id": 25, "title": "Пхукет", "name": "phuket"},
]


@router.get('/hotels', summary="Получить список отелей", description='Дополнительная информация')
def get_hotels( 
    pagination: PaginationDep,
    title: str | None = Query(None, description='Фильтр по названию')
):
    # Фильтрация по названию
    filtered_hotels = hotels
    if title:
        filtered_hotels = [hotel for hotel in hotels if hotel["title"].lower() == title.lower()]
    
    # Пагинация
    start = (pagination.page - 1) * pagination.per_page
    end = start + pagination.per_page
    pagination_hotels = filtered_hotels[start:end]

    return {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": len(filtered_hotels),
        "total_pages": (len(filtered_hotels) + pagination.per_page - 1) // pagination.per_page,  # округление вверх,
        "data": pagination_hotels,
    }
     

@router.delete('/delete_holel/{hotel_id}', summary='Удалить отель', description='Дополнительная информация')
def delete_hotel(
    hotel_id: int
):
    global hotels
    before_len = len(hotels)
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    if len(hotels) == before_len:
        raise(HTTPException(status_code=404, detail='Отель не найден'))
    
    return {
        'message':'deleted',
        }


@router.post('/add_hotel', summary='Добавить отель', description='Дополнительная информация')
def add_hotel(
    hotel_data: Hotel = Body(openapi_examples={
        "1":{"summary":"Мурманск", "value":{"title":"Мурманск", "name":"murmansk-city"}}
    })
):
    hotels.append({'id': len(hotels) + 1, 'title': hotel_data.title, 'name': hotel_data.name})
    return {
        'status': 'OK',
        'message': f'{hotel_data.title} - added'
    }


@router.patch('/edit_hotel/{hotel_id}', summary='Частичное обновление данных', description='Дополнительная информация')
def edit_hotel(
    hotel_id: int,
    hotel_data: HotelPatch
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title is not None:
                hotel['title'] = hotel_data.title
            if hotel_data.name is not None:
                hotel['name'] = hotel_data.name
    return {'status': 'ok'}


@router.put('/put_hotel/{hotel_id}', summary='Полное обновление данных')
def edit_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'], hotel['name'] = hotel_data.title, hotel_data.name
    return {'status': 'ok'}
