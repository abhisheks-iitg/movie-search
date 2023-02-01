from sqlalchemy import create_engine, MetaData, Table, Column, select, and_, text
from sqlalchemy.orm import sessionmaker

from core import application_config
from services.thirdparty.movie_list import Movie


class DBManager:
    """
    Database Manager to encapsulate interaction with the DB
    """

    def __init__(self):
        self.engine = create_engine(application_config.get_db_url())
        self.connection = self.engine.connect()
        meta = MetaData()
        self.movie_list = Table(application_config.get_db_table(), meta,
                                Column('id'),
                                Column('title'),
                                Column('year'),
                                Column('casts'),
                                Column('genres'))
        self.Session = sessionmaker(self.engine)

    def __fetch_movie_by_name(self):
        """
        Fetch all movie list
        :return:
        """
        data = self.connection.execute(self.movie_list.select())
        for mov in data:
            print(mov)

    def get_movie_by_title_and_year(self, file_data):
        """
        Select list of movies based on given title and year
        :param file_data:
        :return:
        """
        select([self.movie_list]).where(and_(self.movie_list.columns.title == file_data['title'],
                                             self.movie_list.columns.year == file_data['year']))

    def create_movie(self, file_data):
        """
        Create and insert record into the DB for the provided input data
        :param file_data:
        :return:
        """
        movie = Movie(file_data['title'], file_data['year'], file_data['cast'], file_data['genres'])

        with self.Session() as session:
            session.add(movie)
            session.commit()
            id_field = movie.id
        return id_field

    def fetch_by_query(self, file_data):
        """
        Fetch result based on SQL Query

        :param file_data:
        :return:
        """
        query = ''
        if file_data['title']:
            query += " title='" + file_data['title'].replace("'", "''") + "' "
        if file_data['year']:
            query += " and year=" + str(file_data['year'])
        if file_data['cast']:
            res = ','.join('\'' + x.replace("'","''") + '\'' for x in file_data['cast'])
            query += " and ARRAY[" + res + "] && casts"

        sql = text(f"SELECT * from movie_list where {query}")
        fetch_query = self.connection.execute(sql)
        results = []
        for data in fetch_query.fetchall():
            movie = Movie(data[1], data[2], data[3], data[4])
            movie.set_id(data[0])
            results.append(movie)
        return results

    def update_record(self, file_data, movie):
        """
        Update existing DB record, based on the provided movie details
        :param file_data:
        :param movie:
        :return:
        """
        casts_value = list(set(movie.casts + file_data['cast']))
        genres_value = list(set(movie.genres + file_data['genres']))
        with self.Session() as session:
            session.query(Movie).filter(Movie.id == movie.id).update(
                {Movie.casts: casts_value, Movie.genres: genres_value}, synchronize_session=False)
            session.commit()

        updated_movie = Movie(movie.title, movie.year, casts_value, genres_value)
        updated_movie.set_id(movie.id)
        return updated_movie
