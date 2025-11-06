import time
import asyncio


def get_data_from_database(query: str):
    """
    Синхронный пример выполнения кода
    Второй запрос ждет, когда завершится первый
    """
    print(f'Получен запрос: {query}')
    if query == 'Сочи':
        time.sleep(4)
    elif query == 'Дубай':
        time.sleep(2)
    print(f"Данные получены")

# get_data_from_database('Сочи')
# get_data_from_database('Дубай')

# Корутина - асинхронная функция
async def get_data_from_database_async(query: str):
    """
    Асинхронный пример выполнения кода
    Мы сразу обрабатываем 2 запроса.
    """
    print(f"Получен запрос: {query}")
    if query == 'Сочи':
        await asyncio.sleep(4)
    elif query == 'Дубай':
        await asyncio.sleep(2)
    print(f"Данные получены: {query}")


async def main():
    await asyncio.gather(
        get_data_from_database_async('Сочи'),
        get_data_from_database_async('Дубай')
    )


asyncio.run(main())
