import requests
import json
import configparser
from create_db import CreateBase
from AddDataTable import AddDataTable


CreateBase()

# Создадим объект парсера параметров настройки
config = configparser.ConfigParser()
config.read("settings.ini")

# Зададим адрес парсинга
url = "https://api-seller.ozon.ru" 
method = config["Ozon-API"]["method"]
print(url + method)

# в head записываем настройки парсинга
head = {
  "Client-Id": config["Ozon-API"]["Client-Id"], 
  "Api-Key": config["Ozon-API"]["Api-Key"],
  "Content-Type": "application/json"
}

# Тело по необходимости можем менять, в зависимости от того, что парсим
# структуру берем из офф источников https://docs.ozon.ru/api/seller/#operation/AnalyticsAPI_AnalyticsGetStockOnWarehouses
body = {
  "limit": "100",
  "offset": "0"
}

body = json.dumps(body)
response = requests.post(url + method, headers=head, data=body)

data = response.json()

# Парсим полученный json, выводим следующую структуру:
#
# Идентификатор склада:
# Категория - Название категории. - Идентификатор товара в системе продавца. - Количество товаров не подлежащих реализации.
for sklad in data['wh_items']:
  for articul in sklad['items']:
    AddDataTable(sklad['name'], articul['category'], articul['barcode'], \
                 articul['sku'], articul['stock']['for_sale'], \
                 articul['stock']['not_for_sale'])
