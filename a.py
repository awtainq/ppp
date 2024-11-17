import requests
import time

# URL сервера
url = "http://niph12.tmweb.ru/index.php"
proxies = {"http": 'http://brd-customer-hl_d6d9728f-zone-datacenter_proxy1:hzzvgl8lcb64@brd.superproxy.io:22225'}
data = {'login':'admin', 'password':"Aaaaaaa"}

for _ in range (20):
    # Измерение времени
    start_time = time.time()  # Начало отсчета
    response = requests.get(url,proxies = proxies)  # Выполнение запроса
    end_time = time.time()  # Конец отсчета

    # Расчет времени ответа
    response_time = end_time - start_time

    # Вывод результата
    print(f"HTTP-статус: {response.status_code}")
    print(f"Время ответа сервера: {response_time:.4f} секунд")
