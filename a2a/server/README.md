# A2A Echo Agent Server

A2A (Agent-to-Agent) Echo Agent Server implementation using Semantic Kernel.

## Overview

This server implements an echo agent that returns the same message it receives. It uses:
- **Semantic Kernel** for AI agent functionality
- **Azure OpenAI Service** for AI model integration
- **uvicorn** as ASGI server
- **EchoPlugin** custom implementation for Semantic Kernel

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```env
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-02-01
SERVER_HOST=localhost
SERVER_PORT=8000
```

3. Update `config.yaml` if needed for additional configuration.

## Running the Server

Basic usage:
```bash
python server.py
```

With custom host and port:
```bash
python server.py --host 0.0.0.0 --port 8080
```

With custom config file:
```bash
python server.py --config custom_config.yaml
```

## Agent Capabilities

1. **echo**: Simple echo that returns the input message
2. **echo_with_prefix**: Echo with a customizable prefix

## Configuration

The server uses both `.env` and `config.yaml` for configuration:
- `.env`: Environment-specific variables (credentials, endpoints)
- `config.yaml`: Application configuration with environment variable substitution