"""

🛠 Что нужно сделать:
Напиши асинхронную функцию fetch_price(product_id: int), которая:

Имитирует HTTP-запрос к магазину: await asyncio.sleep(random.uniform(1, 3))
Возвращает случайную цену: {"product_id": product_id, "price": random.randint(100, 1000)}
Напиши main(), который:

Запрашивает цены для product_id от 1 до 5
Использует asyncio.gather() для параллельного получения всех цен
Выводит общую сумму и время выполнения
Добавь измерение времени (сравни с синхронной версией — бонус!)
"""

import asyncio
import random

async def fetch_price(product_id: int):
    print('Запрос цены...')
    await asyncio.sleep(random.uniform(1, 3))
    return dict(product_id=product_id, price=random.randint(1000, 10000))


async def main():
    result = await asyncio.gather(
        fetch_price(1),
        fetch_price(2),
        fetch_price(3),
        fetch_price(4),
        fetch_price(5),
    )
    print(result)


asyncio.run(main())


