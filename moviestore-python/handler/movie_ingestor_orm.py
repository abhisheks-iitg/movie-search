from core import application_config
from services.aws.s3_manager import S3Manager
from services.thirdparty.db_manager import DBManager
from services.thirdparty.search_manager import SearchManager

s3_manager = S3Manager(application_config.get_region())
db_manager = DBManager()
search_manager = SearchManager()


def lambda_handler(event, context):
    """
    Read event from S3 and persist in DB
    :param event:
    :param context:
    :return:
    """
    bucket = event['detail']['bucket']['name']
    key = event['detail']['object']['key']
    file_data = s3_manager.get_file_content(bucket, key)

    movie_list = db_manager.fetch_by_query(file_data)

    if movie_list:
        if len(movie_list) > 1:
            # Work to merge these entries together.
            raise ValueError("multiple entries found that matches title and year as well as part of cast and genres")
        else:
            movie = db_manager.update_record(file_data, movie_list[0])
            search_manager.delete_index(application_config.get_system_index(), movie_list[0].id)
            search_manager.index(application_config.get_system_index(), movie.id,
                                 {'title': movie.title, 'year': movie.year, 'casts': movie.casts,
                                  'genres': movie.genres})

    else:
        movie_id = db_manager.create_movie(file_data)
        search_manager.index(application_config.get_system_index(), movie_id, file_data)
