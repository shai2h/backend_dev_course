from fastapi import Query, Body, APIRouter, HTTPException
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep

from sqlalchemy import insert, select

from models.hotels import HotelOrm

from database import async_session_maker
from database import engine

router = APIRouter()



@router.get('/hotels', summary="Получить список отелей", description='Дополнительная информация')
async def get_hotels( 
    pagination: PaginationDep,
    title: str | None = Query(None, description='Фильтр по названию')
):
    async with async_session_maker() as session:
        query = select(HotelOrm)
        result = await session.execute(query)

        # магический метод scalars - позволяет забрать 1 элемент из кортежа, т.к. запрос возвращает список из кортежей внутри кортежа 1 значение.
        # all забираем всем кортежи
        hotels = result.scalars().all()
        print(type(hotels), hotels)
        return {'msg:':'OK', 'data:':hotels}

    # if title:
    #     filtered_hotels = [hotel for hotel in hotels if hotel["title"].lower() == title.lower()]
    
    # # Пагинация
    # start = (pagination.page - 1) * pagination.per_page
    # end = start + pagination.per_page
    # pagination_hotels = filtered_hotels[start:end]

    # return {
    #     "page": pagination.page,
    #     "per_page": pagination.per_page,
    #     "total": len(filtered_hotels),
    #     "total_pages": (len(filtered_hotels) + pagination.per_page - 1) // pagination.per_page,  # округление вверх,
    #     "data": pagination_hotels,
    # }
     

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
async def add_hotel(
    hotel_data: Hotel = Body(openapi_examples={
        "1":{"summary":"Мурманск", "value":{"title":"MOSCOW GRAND HOTEL", "location":"г. Москва"}}
    })
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelOrm).values(**hotel_data.model_dump())
        # Логирование SQL-запроса с подставленными значениями для отладки
        # На проде не безопасно светить данные логи
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {
        'status': 'OK',
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
