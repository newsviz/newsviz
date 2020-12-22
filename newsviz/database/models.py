"""
В данном файле описывается структура БД проекта, в данном файле
должно находится описание всех таблиц базы данных.
"""
from sqlalchemy import TIMESTAMP, Column, String
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
    updated_at = Column(TIMESTAMP, nullable=False, server_default=FetchedValue(), server_onupdate=FetchedValue())

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


# Таблица News
class News(BaseModel):
    __tablename__ = "news"
    id = Column(String, primary_key=True)
    date = Column(String)
    topic = Column(String)
    text = Column(String)

    def __repr__(self):
        text = f"{self.text[:100]}..." if len(self.text) > 100 else self.text
        return "<News(date='%s', topic='%s', text='%s')>" % (self.date, self.topic, text)
