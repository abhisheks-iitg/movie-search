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

    if is_invalid_event(file_data):
        # enqueue into the Error Queue
        return

    result_size, _id, movie = db_manager.upsert_orm(file_data)

    if result_size == 0:
        search_manager.index(application_config.get_system_index(), _id, file_data)
    else:
        search_manager.delete_index(application_config.get_system_index(), _id)
        search_manager.index(application_config.get_system_index(), _id,
                             {'title': movie.title, 'year': movie.year, 'cast': movie.casts,
                              'genres': movie.genres})


def is_invalid_event(file_data):
    """
    Function to check and confirm if this is an invalid Event
    :param file_data:
    :return:
    """
    # result = False if year is not a number and title, casts and genre are not alphabets.
    return False
