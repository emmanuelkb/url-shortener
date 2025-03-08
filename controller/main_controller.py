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
    def __init__(self, db_module, cache=None):
        self.__db_module = db_module
        self.__cache = cache


    @exceptions_handler.exceptions_handler
    def shorten_url(self, payload:dict):
        validate(event=payload,schema=schema_validation.shorten_schema)
        short_id = self.generate_short_id()
        payload = {
            'short_id': short_id,
            'long_url': payload['long_url'],
            'counter': 0, # may implement pushing to sqs to handle counter updates
            'created_at': datetime.now().isoformat(),
        }
        response = self.__db_module.put_item(payload)
        if ('ResponseMetadata' in response and 'HTTPStatusCode' in response['ResponseMetadata']
                and response['ResponseMetadata']['HTTPStatusCode'] == HTTPStatus.OK.value):
            if self.__cache:
                self.__cache.cache_key(short_id, payload)
            url = f"{os.environ['API_ENDPOINT']}{short_id}"
            return Response(status_code=201,body=json.dumps({'short_url':url}))


    def fetch_url(self, query_params: dict):
        if 'short_id' not in query_params:
            return Response(
                status_code=HTTPStatus.BAD_REQUEST.value,
                body=json.dumps({'message': 'short_id is required'})
            )
        short_id = query_params['short_id']
        if self.__cache:
            cached_data = self.__cache.retrieve_from_cache(short_id)
            if cached_data:
                return cached_data
        response = self.__db_module.fetch_item(short_id)
        if response and self.__cache:
            self.__cache.cache_key(short_id, response)
        return response


    def redirect(self, short_id:str):
        url = None
        if self.__cache:
            cached_data = self.__cache.retrieve_from_cache(short_id)
            if cached_data:
                url = cached_data['long_url']
        if not url:
            db_response = self.__db_module.fetch_item(short_id)
            if not db_response:
                return Response(status_code=HTTPStatus.NOT_FOUND.value)
            url = db_response['long_url']
            if self.__cache:
                self.__cache.cache_key(short_id, db_response)
        headers = {
            'Location': url,
            'Cache-Control': 'no-cache'
        }
        return Response(status_code=HTTPStatus.TEMPORARY_REDIRECT.value,headers=headers,body='')


    @staticmethod
    def generate_short_id():
        return ''.join(random.sample(string.ascii_letters+string.digits,5))
