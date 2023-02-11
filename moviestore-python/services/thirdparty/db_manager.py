from sqlalchemy import create_engine, MetaData, Table, Column, cast, TEXT
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import sessionmaker

from core import application_config
from services.thirdparty.movie_list import Movie


class DBManager:
    """
    Database Manager to encapsulate interaction with the DB
    """

    def __init__(self):
        self.engine = create_engine(application_config.get_db_url(), echo=True)
        self.connection = self.engine.connect()
        meta = MetaData()
        self.movie_list = Table(application_config.get_db_table(), meta,
                                Column('id'),
                                Column('title'),
                                Column('year'),
                                Column('casts'),
                                Column('genres'))
        self.Session = sessionmaker(self.engine)

    def upsert_orm(self, file_data):
        """
        Fetch result based on Query

        :param file_data:
        :return:
        """

        with self.Session() as session:

            title_year_query = session.query(Movie).filter(Movie.title == file_data['title']).filter \
                (Movie.year == file_data['year'])
            result = []
            if file_data['cast']:
                title_year_cast_query = title_year_query.filter(Movie.casts.overlap(cast(file_data['cast'], ARRAY(TEXT))))
                result = title_year_cast_query.all()
            if len(result) == 0:
                # If no results found with cast-match query, check if there are result matching title and year only.
                # Alternatively, one could query with title and year and do post-processing in code for cast match.
                result = title_year_query.all()
            result_size = len(result)
            if result_size > 1:
                raise ValueError(
                    "multiple entries found that matches title and year as well as part of cast")
            elif result_size == 0:
                # new record, insert into db
                movie = self.create_movie(file_data, session)
            else:
                movie = result[0]
                movie = self.update_record(file_data, movie, session)
            _id = movie.id
            session.commit()
            return result_size, _id, movie

    def create_movie(self, file_data, session):
        """
        Create and insert record into the DB for the provided input data
        :param session:
        :param file_data:
        :return:
        """
        movie = Movie(file_data['title'], file_data['year'], file_data['cast'], file_data['genres'])

        session.add(movie)
        session.flush()
        return movie

    def update_record(self, file_data, movie, session):
        """
        Update existing DB record, based on the provided movie details
        :param session:
        :param file_data:
        :param movie:
        :return:
        """
        casts_value = list(set(movie.casts + file_data['cast']))
        genres_value = list(set(movie.genres + file_data['genres']))
        session.query(Movie).filter(Movie.id == movie.id).update(
            {Movie.casts: casts_value, Movie.genres: genres_value}, synchronize_session=False)

        updated_movie = Movie(movie.title, movie.year, casts_value, genres_value)
        updated_movie.set_id(movie.id)
        return updated_movie
