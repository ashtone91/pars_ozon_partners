import requests
import json
import configparser


# �������� ������ ������� ���������� ���������
config = configparser.ConfigParser()
config.read("settings.ini")

# ������� ����� ��������
url = "https://api-seller.ozon.ru" 
method = config["Ozon-API"]["method"]
print(url + method)

# � head ���������� ��������� ��������
head = {
  "Client-Id": config["Ozon-API"]["Client-Id"], 
  "Api-Key": config["Ozon-API"]["Api-Key"],
  "Content-Type": "application/json"
}

# ���� �� ������������� ����� ������, � ����������� �� ����, ��� ������
# ��������� ����� �� ��� ���������� https://docs.ozon.ru/api/seller/#operation/AnalyticsAPI_AnalyticsGetStockOnWarehouses
body = {
  "limit": "100",
  "offset": "0"
}

body = json.dumps(body)
response = requests.post(url + method, headers=head, data=body)

data = response.json()

# ������ ���������� json, ������� ��������� ���������:
#
# ������������� ������:
# ��������� - �������� ���������. - ������������� ������ � ������� ��������. - ���������� ������� �� ���������� ����������.
for sklad in data['wh_items']:
  print('\n','\n')
  print(sklad['name'], ':', '\n')
  for articul in sklad['items']:
    print(articul['category'],'-', articul['title'],'-',articul['offer_id'],'-',articul['stock']['for_sale'], 'pcs')

