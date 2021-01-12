# Copyright © 2020 Egor Silaev. All rights reserved.

#    This file is part of NewsViz Project.
#
#    NewsViz Project is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    NewsViz Project is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with NewsViz Project.  If not, see <https://www.gnu.org/licenses/>.


"""
Скрипт создает базу данных на локальной машине пользователя,
которые инициировал скрипт. Данный файл должен лежать в той папке,
где планируется лежать база данных
"""
import os

from sqlalchemy import create_engine

# в models.py лежит структура БД, которую надо создавать, поэтому импортируем ее
import models

# TODO: move path to DB in config
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
