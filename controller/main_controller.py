import random
import string
from datetime import datetime
from http import HTTPStatus
from utilities import schema_validation
from aws_lambda_powertools.event_handler import Response
from aws_lambda_powertools.utilities.validation import SchemaValidationError, validate


class MainController:
    def __init__(self, db_module):
        self.db_module = db_module


    def shorten_url(self, payload):
        print(payload)
        validate(event=payload,schema=schema_validation.shorten_schema)
        short_id = self.generate_short_id()
        response = self.db_module.put_item({
            'short_id': short_id,
            'long_url': payload['long_url'],
            'counter': 0,
            'created_at': datetime.now().isoformat(),
        })
        print(response)
        return response

    def fetch_url(self, query_params):
        #Validate payload
        print(query_params)
        response = self.db_module.fetch_item(query_params['short_id'])
        print(response)
        return response

    def redirect(self, short_id):
        print(short_id)
        headers = {
            'Location': 'https://www.apple.com',
            'Cache-Control': 'no-cache'
        }
        return Response(
            status_code=HTTPStatus.TEMPORARY_REDIRECT.value,
            headers=headers,
            body=''
        )

    @staticmethod
    def generate_short_id():
        return ''.join(random.sample(string.ascii_letters+string.digits,5))
