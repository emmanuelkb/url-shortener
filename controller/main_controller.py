import requests

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

    def redirect(self, payload):
        print(payload)
        requests.get('http://apple.com')