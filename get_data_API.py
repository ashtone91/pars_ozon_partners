import requests
import json
import configparser
from create_db import CreateBase
from AddDataTable import AddDataTable
import threading
import time
from datetime import datetime


def ReadDataAPI(body_in, url_in, method_in, head_in):

  body_in = json.dumps(body_in)

  control = True
  while control:

    dt_now = datetime.now()
    current_time = dt_now.strftime("%H:%M:%S")
    current_data = dt_now.strftime("%w/%m/%Y")
    # control = False   

    response = requests.post(url_in + method_in, headers=head_in, data=body_in)

    data = response.json()
    # Парсим полученный json, выводим следующую структуру:
    #
    # Идентификатор склада:
    # Категория - Название категории. - Идентификатор товара в системе продавца. - Количество товаров не подлежащих реализации.
    for sklad in data['wh_items']:
      for articul in sklad['items']:
        AddDataTable(sklad['name'], articul['category'], articul['barcode'], \
                    articul['sku'], articul['stock']['for_sale'], \
                    articul['stock']['not_for_sale'], current_time, current_data)

    print("An entry was made for - ", current_data, "-", current_time)
    time.sleep(30)


if __name__ == "__main__":

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

  readData = threading.Thread(target=ReadDataAPI,  args=(body, url, method, head), daemon=None)
  readData.start()