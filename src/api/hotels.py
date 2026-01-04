from fastapi import Query, Body, APIRouter, HTTPException
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep

from sqlalchemy import insert, select, func

from repositories.hotels import HotelRepository

from models.hotels import HotelOrm

from database import engine
from database import async_session_maker


router = APIRouter()


@router.get('/hotels', summary="Получить список отелей", description='Дополнительная информация')
async def get_hotels(
    paggination: PaginationDep,
    title: str | None = Query(None, description='Описание'),
    location: str | None = Query(None, description='Локация')
):
    async with async_session_maker() as session:
        return await HotelRepository(session).get_all()
    # per_page = paggination.per_page or 5
    # async with async_session_maker() as session:
    #     query = select(HotelOrm)
    #     if title:
    #         query = query.filter(func.lower(HotelOrm.title).contains(title.strip().lower()))
    #     if location:
    #         query = query.filter(func.lower(HotelOrm.location).like(location.strip().lower()))
    #     query = (
    #         query
    #         .limit(per_page)
    #         .offset(paggination.per_page * (paggination.page - 1))
    #     )
    #     # логируем запрос к БД
    #     print(query.compile(compile_kwargs={"literal_binds": True}))

    #     result = await session.execute(query)
    #     hotels = result.scalars().all()
    #     return hotels


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
