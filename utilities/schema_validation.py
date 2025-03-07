shorten_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["long_url"],
  "properties": {
    "long_url": {
      "type": "string",
      "format": "uri",
      "minLength": 1,
      "errorMessage": {
        "type": "The long_url must be a string",
        "format": "Please provide a valid URL including protocol (e.g: https://google.com)",
        "minLength": "URL cannot be empty"
      }
    },
  },
  "additionalProperties": False,
  "errorMessage": {
    "required": {
      "long_url": "The long_url field is required"
    },
    "additionalProperties": "Unknown property detected in the request"
  }
}