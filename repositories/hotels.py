from sqlalchemy import select, func

from repositories.base import BaseRepository
from src.models.hotels import HotelOrm


class HotelRepository(BaseRepository):
    model = HotelOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
        ):
        query = select(HotelOrm)
        if title:
            query = query.filter(func.lower(HotelOrm.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelOrm.location).like(location.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        # логируем запрос к БД
        print(query.compile(compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        return result.scalars().all()
