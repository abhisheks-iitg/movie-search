from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Identity

from core import application_config

Base = declarative_base()


class Movie(Base):
    """
    Entity class to map to the DB based Movie table
    """
    __tablename__ = application_config.get_db_table()
    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    title = Column(String)
    year = Column(Integer)
    casts = Column(ARRAY(String))
    genres = Column(ARRAY(String))

    def __repr__(self):
        return "<Movie(title='{}', year='{}', cast={}, genres={})>" \
            .format(self.title, self.year, self.casts, self.genres)

    def __init__(self, title, year, casts, genres):
        self.title = title
        self.year = year
        self.casts = casts
        self.genres = genres

    def set_id(self, id_field):
        """
        Set id for this movie object
        :param id_field:
        :return:
        """
        self.id = id_field
