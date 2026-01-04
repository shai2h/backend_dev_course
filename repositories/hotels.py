from repositories.base import BaseRepository
from src.models.hotels import HotelOrm


class HotelRepository(BaseRepository):
    model = HotelOrm