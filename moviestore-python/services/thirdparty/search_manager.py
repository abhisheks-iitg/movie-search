import logging
from elasticsearch import Elasticsearch
from core import application_config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SearchManager:
    """
    Search Manager Abstraction for search functionality
    """


    def __init__(self):
        self.es = Elasticsearch(application_config.get_search_server())
        self.doc_type = "_doc"
        """                     ,
                                verify_certs=application_config.is_cert_validated(),
                                http_auth=(
                                application_config.get_search_user(), application_config.get_search_password())"""

    def index(self, index_name, id, doc):
        """
        Index the following document with id into the index_name
        :param index_name:
        :param id:
        :param doc:
        :return:
        """
        return self.es.index(index=index_name, doc_type=self.doc_type, id=id, body=doc)

    def refresh(self, index_name):
        """
        Refresh the index
        :param index_name:
        :return:
        """
        self.es.indices.refresh(index=index_name)

    def search(self, index_name, body):
        """
        Perform Search for the following body contents
        :param index_name:
        :param body:
        :return:
        """
        return self.es.search(index=index_name, doc_type=self.doc_type, body=body)

    def delete_index(self, index_name, id_field):
        """
        delete id based record in the given index
        :param index_name:
        :param id_field:
        :return:
        """
        try:
            self.es.delete(index=index_name, doc_type=self.doc_type, id=id_field)
        except ValueError:
            logger.error("Failed to delete index entry for {id_field} id document")