from fastapi import FastAPI, Query, Body, HTTPException
import uvicorn


app = FastAPI()


hotels = [
    {"id": 1, "title": "Сочи", 'name': "sochi"},
    {"id": 2, "title": "Дубай", 'name': "dubai"},
    {"id": 3, "title": "Москва", 'name': "moskva"},
    {"id": 4, "title": "Казань", 'name': "kazan"},
]

@app.get('/hotels')
def get_hotels(
    title: str | None = Query(None, description='Название отеля')
):
    if title:
        return [hotel for hotel in hotels if hotel["title"].lower() == title.lower()]
    else:
        return hotels
    

@app.delete('/delete_holel/{hotel_id}')
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


@app.post('/add_hotel')
def add_hotel(
    title: str = Body(embed=True), #embed -- возвращает пример ключ:значение & Body - для передачи в теле
):
    hotels.append({'id': len(hotels) + 1, 'title': title})
    return {
        'status': 'OK',
        'message': f'{title} - added'
    }


@app.patch('/edit_hotel/{hotel_id}')
def edit_hotel(
    hotel_id: int,
    title: str | None = Body(None, embed=True),
    name: str | None = Body(None, embed=True)
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = title
            hotel['name'] = name
    return {'status': 'ok'}


@app.put('/put_hotel/{hotel_id}')
def edit_hotel(
    hotel_id: int,
    title: str = Body(embed=True),
    name: str = Body(embed=True)
):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'], hotel['name'] = title, name
    return {'status': 'ok'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)