import boto3


class DynamodbManager:
    """
    Methods to deal with DynamoDB service
    """

    def __init__(self, region):
        self.region = region
        self.dynamodb_client = boto3.resource('dynamodb')

    def insert_item(self, item):
        table = self.dynamodb_client.Table('movie-db')
        table.put_item(Item={
        'title': item['title'],
        'year': item['year'],
        'genre': ['Adventure','Comedy'],
        'cast':['Tom Cruise']
    })