# URL Shortener Service

A serverless URL shortening service built with AWS Lambda, API Gateway, and DynamoDB.

## Overview

This URL shortener service allows you to create shortened URLs that redirect to longer destination URLs. It's built as a serverless application using AWS services and deployed through a CI/CD pipeline.

### Key Features
- Create shortened URLs for any valid long URL
- Retrieve information about existing shortened URLs
- Redirect from shortened URLs to original destinations
- Automatically deployed through AWS CI/CD pipeline

## Architecture

This project is built using the following AWS services:
- **AWS Lambda**: Handles the application logic
- **Amazon API Gateway**: Provides RESTful API endpoints
- **Amazon DynamoDB**: Stores URL mappings
- **AWS CloudFormation/SAM**: Manages infrastructure as code
- **AWS CodePipeline**: Provides CI/CD pipeline for automated deployments
- **AWS ParameterStore**: Stores sensitive credentials
- **Redis**: For Caching
- **AWS SQS**: Queueing Counter Updates (Not implemented Yet)


## Getting Started

### Prerequisites
- AWS Account
- Python 3.12+
- AWS CLI configured
- SAM CLI installed (for local development)
- Git

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/emmanuelkb/url-shortener.git
   cd url-shortener
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up local environment variables:
   ```bash
   export TABLE_NAME=url-shortener-table
   export API_ENDPOINT=http://localhost:3000/
   ```

5. Run tests:
   ```bash
   python -m pytest
   ```

6. For local development with SAM:
   ```bash
   sam build
   sam local start-api
   ```

### Deployment

The project uses a CI/CD pipeline for automated deployment:

1. Push changes to the GitHub repository
2. AWS CodePipeline automatically detects changes
3. CodeBuild builds the application
4. CloudFormation deploys the stack

To manually deploy:

```bash
sam build
sam deploy --guided
```

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /shorten | Create a new shortened URL |
| GET | /urls | Retrieve information about a shortened URL |
| GET | /{short_id} | Redirect to the original URL |
| DELETE | /delete-url | Delete a shortened URL |

### Example Usage

#### Create a Shortened URL
```bash
curl -X POST \
  https://your-api-gateway-url/Prod/shorten \
  -H 'Content-Type: application/json' \
  -d '{"long_url": "https://example.com/very-long-url-that-needs-shortening"}'
```

Response:
```json
{
  "short_url": "https://your-api-gateway-url/Prod/Cx2N7e"
}
```

#### Get URL Information
```bash
curl -X GET \
  https://your-api-gateway-url/Prod/urls?short_id=Cx2N7e
```

#### Access Shortened URL
Simply visit `https://your-api-gateway-url/Prod/Cx2N7e` in a browser and you'll be redirected to the original URL.

## Testing

The project includes tests for verifying the functionality of the URL shortener. To run tests:

```bash
python -m pytest
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| TABLE_NAME | DynamoDB table name for storing URLs |
| API_ENDPOINT | Base URL for the shortened links |

## CI/CD Pipeline

The project uses AWS CodePipeline for continuous integration and deployment:

1. Source stage: Pulls code from GitHub repository
2. Build stage: Builds the application using CodeBuild
3. Deploy stage: Deploys the application using CloudFormation

## License

[MIT License](LICENSE)
