import json

import botocore
from aws_lambda_powertools.utilities.validation import SchemaValidationError
from aws_lambda_powertools.event_handler import Response

def exceptions_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SchemaValidationError as e:
            return Response(status_code=400, body=json.dumps({'message':str(e)}))
    return wrapper

