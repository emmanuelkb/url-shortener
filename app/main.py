from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

# Initializations outside handler to keep warm
tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()

@app.post("/shorten")
def create_url():
    ...

@app.get("/urls")
def fetch_all_urls():
    ...

@app.delete("/delete-url")
def create_url():
    ...

def lambda_handler(event: dict, context: LambdaContext) -> dict:
    print(event)
    print(context)
    return app.resolve(event, context)