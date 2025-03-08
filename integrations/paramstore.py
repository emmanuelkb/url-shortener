import json
import boto3
from botocore.exceptions import ClientError


class ParameterStore:

    def __init__(self, region_name='eu-west-1'):
        self.__ssm_client = boto3.client('ssm', region_name=region_name)

    def put_parameter(self, name, value, description=None, secure=False, overwrite=True):
        try:
            params = {
                'Name': name,
                'Value': value,
                'Type': 'SecureString' if secure else 'String',
                'Overwrite': overwrite
            }
            if description:
                params['Description'] = description
            response = self.__ssm_client.put_parameter(**params)
            print(response)
            return True
        except ClientError as e:
            print(f"Error storing parameter {name}: {e}")
            return False

    def get_parameter(self, name, with_decryption=True):
        try:
            response = self.__ssm_client.get_parameter(
                Name=name,
                WithDecryption=with_decryption
            )
            return json.loads(response['Parameter']['Value'])
        except ClientError as e:
            print(f"Error retrieving parameter {name}: {e}")
            return None


    def delete_parameter(self, name):
        try:
            self.__ssm_client.delete_parameter(Name=name)
            print(f"Successfully deleted parameter {name}")
            return True
        except ClientError as e:
            print(f"Error deleting parameter {name}: {e}")
            return False
