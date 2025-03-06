from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from integrations.dynamodb import  DynamoDB
from controller import main_controller

# Initializations outside handler to keep warm
# tracer = Tracer()
# logger = Logger()
DB_CLIENT = DynamoDB()
APP = APIGatewayRestResolver()
CONTROLLER = main_controller.MainController(DB_CLIENT)

@APP.post("/shorten")
def create_url():
    return CONTROLLER.shorten_url(APP.current_event.body)

@APP.get("/urls")
def fetch_all_urls():
    return CONTROLLER.fetch_url(APP.current_event.query_string_parameters)

@APP.delete("/delete-url")
def delete_url():
    ...

@APP.get("/abcde")
def redirect_url():
    return CONTROLLER.redirect(APP.current_event.body)

def lambda_handler(event: dict, context: LambdaContext) -> dict:
    print(event)
    print(context)
    return APP.resolve(event, context)