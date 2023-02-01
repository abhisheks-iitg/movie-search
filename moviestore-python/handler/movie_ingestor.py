from services.aws.s3_manager import S3Manager
from services.aws.dynamodb_manager import DynamodbManager
from services.thirdparty.search_manager import SearchManager

from datetime import datetime
import psycopg2
def lambda_handler(event, context):
    """
    Read event from S3 and persist in DB
    :param event:
    :param context:
    :return:
    """
    bucket = event['detail']['bucket']['name']
    key = event['detail']['object']['key']
    s3Manager = S3Manager('eu-west-2')
    file_data = s3Manager.get_file_content(bucket, key)

    """dynamodb = DynamodbManager('eu-west-2')
    dynamodb.insert_item(file_data)
    print(file_data)
    """

    conn = psycopg2.connect(database="moviedb", user="postgres", password="postgres", host="127.0.0.1", port="5432")
    print ("Opened database successfully")

    cur = conn.cursor()

    cur.execute("INSERT INTO test (a) \
          VALUES (200)");

    conn.commit()
    print(   "Records created successfully")
    conn.close()

    """searchManager = SearchManager()


    doc = {
        'author': 'Abhishek',
        'text': 'Interensting content...',
        'timestamp': datetime.now(),
    }
    resp = searchManager.index("test-index", 8, doc)
    print(resp['result'])

    doc = {
        'author': 'Srivastava',
        'text': 'Interensting content 2...',
        'timestamp': datetime.now(),
    }
    resp = searchManager.index("test-index", 9, doc=doc)

    print(resp['result'])

    searchManager.refresh("test-index")

    resp = searchManager.search('test-index', body={
        'query': {
            'match': {
                'author': 'Srivastava',
            }
        }
    })

    print(resp)
    """