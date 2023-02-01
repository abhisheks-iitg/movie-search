"""
Core interface for reading secrets from AWS Secret Manager or other 3rd party secret vaults.
"""


@staticmethod
def get_search_user():
    """
    retrieve user for connecting to Search Cluster. ElasticSearch in current implementation
    :return:
    """
    return "elastic"


@staticmethod
def get_search_password():
    """
    Retrieve password for connecting to Search Cluster. ElasticSearch in current implementation
    :return:
    """
    return "Cyc+=XxyMJMFqr6LgJfB"
