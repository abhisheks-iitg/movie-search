from core import secret_store

"""
Centralized Configuration Sub-System for the Application
"""


@staticmethod
def get_search_server():
    return 'https://localhost:9200'


@staticmethod
def is_cert_validated():
    return False


@staticmethod
def get_search_user():
    return secret_store.get_search_user()


@staticmethod
def get_search_password():
    return secret_store.get_search_password()


@staticmethod
def get_db_url():
    return 'postgresql://postgres:postgres@localhost/moviedb'


@staticmethod
def get_db_table():
    return 'movie_list'


@staticmethod
def get_region():
    return 'eu-west-2'


def get_system_index():
    return "abhisheks"