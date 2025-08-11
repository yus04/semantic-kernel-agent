# Testing Guide for A2A Echo Agent

This guide provides instructions for testing the A2A Echo Agent implementation.

## Prerequisites

Install the required dependencies for either server or client:

### Server Dependencies
```bash
cd a2a/server
pip install -r requirements.txt
```

### Client Dependencies
```bash
cd a2a/client
pip install -r requirements.txt
```

## Configuration

### Azure OpenAI Setup
Before running the server, configure your Azure OpenAI credentials:

1. Copy the `.env` file to `.env.local`:
```bash
cd a2a/server
cp .env .env.local
```

2. Edit `.env.local` with your actual credentials:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-02-01
SERVER_HOST=localhost
SERVER_PORT=8000
```

3. Load the local environment:
```bash
source .env.local
```

## Running Tests

### 1. Basic Functionality Test
Run the included test script to verify basic functionality:
```bash
python /tmp/test_a2a_simple.py
```

### 2. Manual Server Testing
Start the server:
```bash
cd a2a/server
python server.py
```

In another terminal, test the endpoints:
```bash
# Check server status
curl http://localhost:8000/

# Get AgentCard
curl http://localhost:8000/agent/card

# Test echo functionality
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World!", "capability": "echo"}'

# Test echo with prefix
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World!", "capability": "echo_with_prefix", "parameters": {"prefix": "Bot: "}}'
```

### 3. Client Testing
With the server running, test the client:
```bash
cd a2a/client

# Check server health
python client.py health

# Get agent information
python client.py info

# Send a simple echo message
python client.py echo "Hello there!"

# Send echo with custom prefix
python client.py echo "How are you?" --capability echo_with_prefix --prefix "Robot: "

# Interactive mode
python client.py interactive
```

## Expected Outputs

### AgentCard Response
```json
{
  "agent_id": "echo-agent-v1",
  "name": "EchoAgent",
  "description": "An echo agent that returns the same message it receives using Semantic Kernel",
  "version": "1.0.0",
  "capabilities": [
    {
      "name": "echo",
      "description": "Echoes back the input message"
    },
    {
      "name": "echo_with_prefix", 
      "description": "Echoes back the input message with a prefix"
    }
  ]
}
```

### Echo Response
```json
{
  "response": "Hello World!",
  "agent_id": "echo-agent-v1",
  "capability_used": "echo"
}
```

### Echo with Prefix Response
```json
{
  "response": "Bot: Hello World!",
  "agent_id": "echo-agent-v1", 
  "capability_used": "echo_with_prefix"
}
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install missing dependencies using pip
2. **Azure OpenAI Connection Error**: Verify credentials and endpoint configuration
3. **Server Not Reachable**: Ensure server is running and accessible
4. **Port Already in Use**: Use `--port` parameter to specify different port

### Debugging

Enable debug mode by setting `debug: true` in `config.yaml` or by checking server logs for detailed error information.

### Health Check

Always verify server health before testing:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "agent": "EchoAgent"
}
```