import json
import os
import random
import string
from datetime import datetime
from http import HTTPStatus
from utilities import schema_validation,exceptions_handler
from aws_lambda_powertools.event_handler import Response
from aws_lambda_powertools.utilities.validation import validate

class MainController:
    def __init__(self, db_module):
        self.db_module = db_module

    @exceptions_handler.exceptions_handler
    def shorten_url(self, payload:dict):
        # Todo: Implement caching and counter update
        validate(event=payload,schema=schema_validation.shorten_schema)
        short_id = self.generate_short_id()
        response = self.db_module.put_item({
            'short_id': short_id,
            'long_url': payload['long_url'],
            'counter': 0,
            'created_at': datetime.now().isoformat(),
        })
        if ('ResponseMetadata' in response and 'HTTPStatusCode' in response['ResponseMetadata']
                and response['ResponseMetadata']['HTTPStatusCode'] == HTTPStatus.OK.value):
            url = f"{os.environ['API_ENDPOINT']}{short_id}"
            return Response(status_code=201,body=json.dumps({'short_url':url}))

    def fetch_url(self, query_params:dict):
        #Validate payload
        print(query_params)
        response = self.db_module.fetch_item(query_params['short_id'])
        print(response)
        return response

    def redirect(self, short_id:str):
        # Todo: Implement caching and counter update
        response = self.db_module.fetch_item('Cx2N7e')
        if not response:
            return  Response(
            status_code=HTTPStatus.NOT_FOUND.value
        )
        headers = {
            'Location': response['long_url'],
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
