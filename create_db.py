import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error

try:
    # Подключение к серверу
    connection = psycopg2.connect(user='postgres', password='1111', host='127.0.0.1')

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Получение курсора
    cursor = connection.cursor()

    sql_create_database = 'create database ozon_pars'

    cursor.execute(sql_create_database)
except (Exception, Error) as error:
    print("Error work to PostgresSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Connection close")
