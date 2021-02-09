"""
Скрипт создает базу данных на локальной машине пользователя,
которые инициировал скрипт. Данный файл должен лежать в той папке,
где планируется лежать база данных
"""
import os

from sqlalchemy import create_engine

# в models.py лежит структура БД, которую надо создавать, поэтому импортируем ее
import models

DB_NAME = "newsviz.sqlite"

# Инициируем нашу базу данных с именем DB_NAME
# Если нужно создать базу данных в оперативной памяти, а не на диске, то
# вместо {DB_NAME} указываем :memory:, т.е. вот так engine наш выглядит будет
# так: sqlite:///:memory:
engine = create_engine(f"sqlite:///{DB_NAME}", echo=True)
if os.path.exists(DB_NAME):
    print("База данных уже существует")
else:
    models.Base.metadata.create_all(engine)
    print("База данных успешно создана")
