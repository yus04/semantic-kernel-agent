# Semantic Kernel Agent - A2A Implementation

This repository contains an A2A (Agent-to-Agent) sample implementation using Semantic Kernel, demonstrating how to build agents that can communicate with each other.

## Overview

The project implements:
- **A2A Echo Agent Server**: Uses Semantic Kernel with Azure OpenAI Service
- **A2A Client**: Command-line interface for interacting with the agent
- **EchoPlugin**: Custom Semantic Kernel plugin for echo functionality
- **AgentCard**: A2A standard agent discovery and capability description

## Architecture

```
a2a/
├── server/          # Echo Agent Server
│   ├── server.py    # FastAPI server with Semantic Kernel
│   ├── echo_plugin.py     # Custom Semantic Kernel plugin
│   ├── agent_card.py      # AgentCard implementation
│   ├── config.yaml        # Server configuration
│   ├── .env              # Environment variables
│   └── requirements.txt   # Server dependencies
└── client/          # A2A Client
    ├── client.py    # Command-line client
    ├── config.yaml  # Client configuration
    ├── .env         # Environment variables
    └── requirements.txt   # Client dependencies
```

## Quick Start

### 1. Setup Server

```bash
cd a2a/server
pip install -r requirements.txt

# Configure your Azure OpenAI credentials in .env
cp .env .env.local
# Edit .env.local with your Azure OpenAI details

# Start the server
python server.py
```

### 2. Setup Client

```bash
cd a2a/client
pip install -r requirements.txt

# Test the connection
python client.py health

# Get agent information
python client.py info

# Send a message
python client.py echo "Hello World!"

# Interactive mode
python client.py interactive
```

## Features

### Server Features
- **Semantic Kernel Integration**: Uses Semantic Kernel for AI agent functionality
- **Azure OpenAI Service**: Integrates with Azure OpenAI for AI capabilities
- **FastAPI Framework**: RESTful API with automatic documentation
- **AgentCard Support**: Standard A2A agent discovery
- **EchoPlugin**: Custom plugin demonstrating Semantic Kernel extensibility
- **Configurable**: Environment-based configuration with YAML support

### Client Features
- **Command-line Interface**: Easy-to-use CLI for agent interaction
- **Interactive Mode**: Real-time chat with the agent
- **AgentCard Retrieval**: Automatic discovery of agent capabilities
- **Health Monitoring**: Server health check functionality
- **Flexible Configuration**: Environment-based configuration

### Agent Capabilities
1. **echo**: Simple echo that returns the input message
2. **echo_with_prefix**: Echo with a customizable prefix

## Configuration

Both server and client use environment variables and YAML configuration:

### Server Configuration (.env)
```env
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-02-01
SERVER_HOST=localhost
SERVER_PORT=8000
```

### Client Configuration (.env)
```env
SERVER_URL=http://localhost:8000
```

## API Documentation

When the server is running, visit:
- API Documentation: http://localhost:8000/docs
- AgentCard: http://localhost:8000/agent/card
- Health Check: http://localhost:8000/health

## Examples

### Basic Echo
```bash
$ python client.py echo "Hello there!"
Response: Hello there!
```

### Echo with Prefix
```bash
$ python client.py echo "How are you?" --capability echo_with_prefix --prefix "Bot: "
Response: Bot: How are you?
```

### Agent Information
```bash
$ python client.py info
Agent Name: EchoAgent
Agent ID: echo-agent-v1
Description: An echo agent that returns the same message it receives using Semantic Kernel
Version: 1.0.0

Capabilities:
  - echo: Echoes back the input message
  - echo_with_prefix: Echoes back the input message with a prefix
```

## Requirements

- Python 3.8+
- Azure OpenAI Service account
- Dependencies listed in requirements.txt files

## References

- [A2A Project Official Repository](https://github.com/a2aproject/a2a-python)
- [Semantic Kernel A2A Sample](https://github.com/mathminds/a2a/tree/main/samples/python/agents/semantickernel)
- [Microsoft Semantic Kernel](https://github.com/microsoft/semantic-kernel)