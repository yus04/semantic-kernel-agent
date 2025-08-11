# A2A Echo Agent Client

A2A (Agent-to-Agent) Client for interacting with the Echo Agent Server.

## Overview

This client provides a command-line interface to interact with the A2A Echo Agent Server. Features include:
- AgentCard retrieval
- Message sending with different capabilities
- Interactive chat mode
- Health check functionality

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```env
SERVER_URL=http://localhost:8000
```

3. Update `config.yaml` if needed for additional configuration.

## Usage

### Command Line Interface

Get agent information:
```bash
python client.py info
```

Send a simple echo message:
```bash
python client.py echo "Hello World!"
```

Send echo with prefix:
```bash
python client.py echo "Hello World!" --capability echo_with_prefix --prefix "Robot: "
```

Check server health:
```bash
python client.py health
```

### Interactive Mode

Start interactive chat:
```bash
python client.py interactive
```

In interactive mode, you can:
- Type messages to chat with the agent
- Use `info` to display agent information
- Use `/prefix <text>` to set a prefix for subsequent messages
- Use `/clear` to remove the current prefix
- Type `quit` to exit

### Custom Configuration

Use a different config file:
```bash
python client.py --config custom_config.yaml info
```

## Examples

Basic echo:
```bash
$ python client.py echo "Hello there!"
Response: Hello there!
```

Echo with prefix:
```bash
$ python client.py echo "How are you?" --capability echo_with_prefix --prefix "Bot says: "
Response: Bot says: How are you?
```

Interactive session:
```bash
$ python client.py interactive
A2A Echo Agent Interactive Mode
Type 'quit' to exit, 'info' for agent information
Use '/prefix <prefix>' to set a prefix for echo_with_prefix
--------------------------------------------------
You: Hello!
Agent: Hello!
You: /prefix Echo Bot: 
Prefix set to: 'Echo Bot: '
You: How are you?
Agent: Echo Bot: How are you?
You: quit
```

## Configuration

The client uses both `.env` and `config.yaml` for configuration:
- `.env`: Environment-specific variables (server URL)
- `config.yaml`: Application configuration with environment variable substitution