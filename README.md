# Stacksync - Take Home Assignment
A containerized Flask application to execute Python scripts in a nsjail-restricted environment.

### Stack
- Python (Flask)
- nsjail
- Docker
- Google Cloud Run

## Deployed on Google Cloud Run
Test service with

`curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    print(\"Hello from stdout\")\n    return {\"message\": \"Hello from Cloud Run\"}"}' \
  https://stacksync-test-553500313772.us-south1.run.app/execute`
  
Expected Response

`{"result":{"message":"Hello from Cloud Run"},"stdout":"Hello from stdout\n\n"}`

## Running locally
Run the server locally as a docker container using the following command

`sudo docker build -t script-executor . & sudo docker run -p 9090:8080 script-executor`

Test with

`curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    print(\"Hello from stdout\")\n    return {\"message\": \"Hello from Cloud Run\"}"}' \
  http://localhost:9090/execute`

## Features
Accepts `POST` requests to `/execute` with JSON payload:

`{
    "script": "def main():\n    import json\n    print('hello world')\n    data = {\"message\": \"Hello from user script\", \"status\": \"success\"}\n    return [\"hbde\"]\n\n"
}`

- Validates user scripts.
- Writes scripts to a temporary file and loads them via a wrapper module.
- Returns output of main() as a JSON object and stdout as part of the response.
- Includes error trace in stdout if execution fails.
- Output format
  `{"result": "...", "stdout": "..."}`

## Future Development
- Cache and other optimizations to offset cold start issues
- Integrate databases to maintain per user executions and history or for business purposes
- Distribute infra to run independent requests in parallel, especially since these services for all practical purposes are stateless
- Ability to provide custom requirements to expand modules and libraries that may be used