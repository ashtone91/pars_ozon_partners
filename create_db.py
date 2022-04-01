import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error


def CreateBase():
    try:
        # Подключение к серверу
        connection = psycopg2.connect(user='postgres', password='1111', host='127.0.0.1')
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Получение курсора
        cursor = connection.cursor()   

        #-----------------------------------------------------------------------------------
        # Проверяем существование базы данных, если нет - создаем её
        #-----------------------------------------------------------------------------------
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'ozon_pars'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('CREATE DATABASE ozon_pars')   
            print("CREATE DATABASE - OK") 

    except (Exception, Error) as error:
        print("Error create DATABASE PostgresSQL", error)
    finally:
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            print("success - CREATE DATABASE")
            CreateTable()


def CreateTable():
    try:
        # Подключение к базе данных
        connection = psycopg2.connect(user='postgres', password='1111', host='127.0.0.1', database="ozon_pars", port="5432")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()   

        #-----------------------------------------------------------------------------------
        # Проверяем существование таблицы, если нет - создаем её
        #-----------------------------------------------------------------------------------
        sql_create_table = "CREATE TABLE leftovers_in_warehouse( id SERIAL, \
                            name_sklad VARCHAR,     \
                            category VARCHAR,       \
                            barcode VARCHAR,        \
                            sku INTEGER,         \
                            for_sale INTEGER,    \
                            not_for_sale INTEGER,  \
                            date_read VARCHAR,      \
                            time_read VARCHAR)"

        cursor.execute("SELECT * FROM pg_catalog.pg_tables WHERE schemaname = 'leftovers_in_warehouse'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(sql_create_table)
            print("CREATE TABLE - OK") 

        
    except (Exception, Error) as error:
        print("Error CREATE TABLE to PostgresSQL", error)
    finally:
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            print("success - CREATE TABLE")


