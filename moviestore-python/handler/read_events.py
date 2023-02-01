from datetime import datetime

from services.aws.dynamodb_manager import DynamodbManager
from services.aws.s3_manager import S3Manager
from services.thirdparty.search_manager import SearchManager


def lambda_handler(event, context):
    """
    Read event from S3 and persist in DB
    :param event:
    :param context:
    :return:
    """
    bucket = event['detail']['bucket']['name']
    key = event['detail']['object']['key']
    s3_manager = S3Manager('eu-west-2')
    file_data = s3_manager.get_file_content(bucket, key)

    dynamodb = DynamodbManager('eu-west-2')
    dynamodb.insert_item(file_data)
    print(file_data)

    search_manager = SearchManager()

    doc = {
        'author': 'Abhishek',
        'text': 'Interensting content...',
        'timestamp': datetime.now(),
    }
    resp = search_manager.index("test-index", 8, doc)
    print(resp['result'])

    doc = {
        'author': 'Srivastava',
        'text': 'Interensting content 2...',
        'timestamp': datetime.now(),
    }
    resp = search_manager.index("test-index", 9, doc=doc)

    print(resp['result'])

    search_manager.refresh("test-index")

    resp = search_manager.search('test-index', body={
        'query': {
            'match': {
                'author': 'Srivastava',
            }
        }
    })

    print(resp)
