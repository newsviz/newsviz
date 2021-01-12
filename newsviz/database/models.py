# Copyright © 2020 Egor Silaev. All rights reserved.
# Copyright © 2021 Sviatoslav Kovalev. All rights reserved.

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
В данном файле описывается структура БД проекта, в данном файле
должно находится описание всех таблиц базы данных.
"""
from sqlalchemy import TIMESTAMP, Column, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import FetchedValue

Base = declarative_base()


class BaseModel(Base):
    """
    Абстрактный класс, описывающий все поля общие для всех таблиц. От
    него будут наследоваться остальные классы наших таблиц
    """

    __abstract__ = True

    created_at = Column(TIMESTAMP, nullable=False, server_default=FetchedValue())
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=FetchedValue(),
        server_onupdate=FetchedValue(),
    )

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Raw(BaseModel):
    __tablename__ = "raw"
    id = Column(String, primary_key=True)
    date = Column(DateTime)
    topic = Column(String)
    text = Column(Text)

    def __repr__(self):
        text = f"{self.text[:97]}..." if len(self.text) > 100 else self.text
        return "<RAW(date='{}', topic='{}', text='{}')>".format(
            self.date, self.topic, text
        )


class Processed(BaseModel):
    __tablename__ = "processed"
    id = Column(String, primary_key=True)
    lemmatized = Column(Text)

    def __repr__(self):
        text = (
            f"{self.lemmatized[:97]}..."
            if len(self.lemmatized) > 100
            else self.lemmatized
        )
        return "<PROCESSED(lemmatized='{}')>".format(text)
