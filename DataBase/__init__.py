from datetime import datetime, timedelta

import peewee
from peewee import *
from loguru import logger

config_base = {
    "type": "sqlite3",
    "dbname": "wildberries",
    "user": "",
    "password": "",
    "host": "",
    "port": ""
}


def get_base_client():
    """
    Подключает клиент базы данных по настройкам,
    заданным в файле.
    :path: - Путь файла конфигураций

    Обязательными полями являются параметры:
    :type: - один из типов 'sqlite3', 'mysql'
    :dbname: - название базы данных
    Для MySQL должны быть указаны параметры:
    :user: - логин
    :password: - пароль
    :host: - хост
    :port: - порт

    Возвратит один из двух клиентов(SQLite3, MySql).
    В случае несоответствия параметров вызовет Exception/
    :return:
    """

    base = config_base

    if base['type'] == 'sqlite3':
        name = f'../{base["dbname"]}.{base["type"]}'
        db = SqliteDatabase(name)

    elif base['type'] == 'mysql':
        db = MySQLDatabase(
            base['dbname'],
            user=base['user'],
            password=base['password'],
            host=base['host'],
            port=base['port'],
        )
    else:
        raise Exception
    return db


logger.info(f"Connect to data base {config_base['dbname']}")
data_base = get_base_client()
cursor = data_base.cursor()
