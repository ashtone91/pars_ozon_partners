import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
import requests
import json
import configparser


def AddDataTable(name_sklad, category, barcode, sku, for_sale, not_for_sale):
    try:
        # Подключение к базе данных
        connection = psycopg2.connect(user='postgres', password='1111', host='127.0.0.1', database="ozon_pars", port="5432")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()   

        #-----------------------------------------------------------------------------------
        # Добавляем запись в таблицу
        #-----------------------------------------------------------------------------------
        sql_add_data = "INSERT INTO leftovers_in_warehouse VALUES (DEFAULT, '" + name_sklad + "', '"   \
                                + category + "', '"     \
                                + barcode + "', "      \
                                + str(sku) + ", "          \
                                + str(for_sale) + ", "     \
                                + str(not_for_sale) + ")" 

        cursor.execute(sql_add_data)
        
    except (Exception, Error) as error:
        print("Error ADD DATA to PostgresSQL", error)
    finally:
        if connection:
            connection.commit()
            cursor.close()
            connection.close()


