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
def fetch_url():
    return CONTROLLER.fetch_url(APP.current_event.query_string_parameters)

@APP.delete("/delete-url")
def delete_url():
    ...

@APP.get("/<short_id>")
def redirect_url(short_id:str):
    return CONTROLLER.redirect(short_id)

def lambda_handler(event: dict, context: LambdaContext) -> dict:
    print(event)
    print(context)
    return APP.resolve(event, context)