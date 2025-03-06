from aws_lambda_powertools.event_handler import Response
from http import HTTPStatus

class MainController:
    def __init__(self, db_module):
        self.db_module = db_module


    def shorten_url(self, payload):
        #Validate payload
        print(payload)
        response = self.db_module.put_item({
            'short_id': 'abcde',
            'long_url': 'www.facebook.com',
            'counter': 0})
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