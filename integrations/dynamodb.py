import os
import boto3

class DynamoDB:
    def __init__(self):
        self.__resource = boto3.resource('dynamodb')
        self.__table = self.__resource.Table(os.environ['TABLE_NAME'])

    def fetch_item(self, short_id):
        try:
            response = self.__table.get_item(
                Key={
                    'short_id' : short_id
                })
            if 'Item' in response:
                print("item found")
                return response['Item']
            else:
                print("item not found")
                return {}
        except Exception as e:
            print("Error getting item:", str(e))



    def put_item(self,payload):
        try:
            return self.__table.put_item(Item=payload)
        except Exception as e:
            print("Error adding item to table:", str(e))
