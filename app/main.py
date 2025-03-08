# from aws_lambda_powertools import Logger, Tracer
import os
from controller import main_controller
from integrations.dynamodb import  DynamoDB
from integrations.paramstore import  ParameterStore
from integrations.redis_integration import RedisCache
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

# Initializations outside handler to keep warm
# tracer = Tracer()
# logger = Logger()
DB_CLIENT = DynamoDB()
SSM_CLIENT = ParameterStore()
REDIS_CONFIG = SSM_CLIENT.get_parameter(os.environ['REDIS_CONFIG'])
REDIS_CLIENT = RedisCache(REDIS_CONFIG)
APP = APIGatewayRestResolver()
CONTROLLER = main_controller.MainController(DB_CLIENT,cache=REDIS_CLIENT)

@APP.post("/shorten")
def create_url():
    return CONTROLLER.shorten_url(APP.current_event.json_body)

@APP.get("/urls")
def fetch_url():
    return CONTROLLER.fetch_url(APP.current_event.query_string_parameters)

@APP.get("/<short_id>")
def redirect_url(short_id:str):
    return CONTROLLER.redirect(short_id)

def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return APP.resolve(event, context)