"""
A2A Echo Client implementation
"""
import os
import yaml
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import click


class A2AClient:
    """
    A2A Client for interacting with the Echo Agent
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # Substitute environment variables in config
        self._substitute_env_vars(self.config)
        
        # Server URL
        self.server_url = self.config["server"]["url"]
        
        # Agent card cache
        self._agent_card = None

    def _substitute_env_vars(self, obj):
        """Recursively substitute environment variables in config"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self._substitute_env_vars(value)
        elif isinstance(obj, list):
            return [self._substitute_env_vars(item) for item in obj]
        elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
            env_var = obj[2:-1]
            return os.getenv(env_var, obj)
        return obj

    def get_agent_card(self) -> Optional[Dict[str, Any]]:
        """
        Get the AgentCard from the server
        
        Returns:
            AgentCard dictionary or None if failed
        """
        try:
            response = requests.get(f"{self.server_url}/agent/card")
            response.raise_for_status()
            self._agent_card = response.json()
            return self._agent_card
        except requests.RequestException as e:
            print(f"Error getting agent card: {e}")
            return None

    def invoke_agent(self, message: str, capability: str = "echo", parameters: Dict[str, Any] = None) -> Optional[str]:
        """
        Invoke the agent with a message
        
        Args:
            message: The message to send to the agent
            capability: The capability to use (default: "echo")
            parameters: Additional parameters for the capability
            
        Returns:
            The response from the agent or None if failed
        """
        if parameters is None:
            parameters = {}
            
        try:
            payload = {
                "message": message,
                "capability": capability,
                "parameters": parameters
            }
            
            response = requests.post(
                f"{self.server_url}/agent/invoke",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response")
            
        except requests.RequestException as e:
            print(f"Error invoking agent: {e}")
            return None

    def check_server_health(self) -> bool:
        """
        Check if the server is healthy
        
        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = requests.get(f"{self.server_url}/health")
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False

    def display_agent_info(self):
        """Display information about the agent"""
        agent_card = self.get_agent_card()
        if not agent_card:
            print("Failed to retrieve agent card")
            return
        
        print(f"Agent Name: {agent_card['name']}")
        print(f"Agent ID: {agent_card['agent_id']}")
        print(f"Description: {agent_card['description']}")
        print(f"Version: {agent_card['version']}")
        print("\nCapabilities:")
        for capability in agent_card['capabilities']:
            print(f"  - {capability['name']}: {capability['description']}")


@click.group()
@click.option('--config', default='config.yaml', help='Configuration file path')
@click.pass_context
def cli(ctx, config):
    """A2A Echo Client CLI"""
    ctx.ensure_object(dict)
    ctx.obj['client'] = A2AClient(config_path=config)


@cli.command()
@click.pass_context
def info(ctx):
    """Display agent information"""
    client = ctx.obj['client']
    
    if not client.check_server_health():
        print("Error: Server is not reachable. Please ensure the server is running.")
        return
    
    client.display_agent_info()


@cli.command()
@click.argument('message')
@click.option('--capability', default='echo', help='Capability to use (echo, echo_with_prefix)')
@click.option('--prefix', help='Prefix for echo_with_prefix capability')
@click.pass_context
def echo(ctx, message, capability, prefix):
    """Send a message to the echo agent"""
    client = ctx.obj['client']
    
    if not client.check_server_health():
        print("Error: Server is not reachable. Please ensure the server is running.")
        return
    
    parameters = {}
    if capability == "echo_with_prefix" and prefix:
        parameters["prefix"] = prefix
    
    response = client.invoke_agent(message, capability, parameters)
    if response:
        print(f"Response: {response}")
    else:
        print("Failed to get response from agent")


@cli.command()
@click.pass_context
def interactive(ctx):
    """Interactive mode for chatting with the echo agent"""
    client = ctx.obj['client']
    
    if not client.check_server_health():
        print("Error: Server is not reachable. Please ensure the server is running.")
        return
    
    print("A2A Echo Agent Interactive Mode")
    print("Type 'quit' to exit, 'info' for agent information")
    print("Use '/prefix <prefix>' to set a prefix for echo_with_prefix")
    print("-" * 50)
    
    current_prefix = None
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'info':
                client.display_agent_info()
                continue
            elif user_input.startswith('/prefix '):
                current_prefix = user_input[8:]
                print(f"Prefix set to: '{current_prefix}'")
                continue
            elif user_input.startswith('/clear'):
                current_prefix = None
                print("Prefix cleared")
                continue
            
            # Choose capability based on whether prefix is set
            if current_prefix:
                capability = "echo_with_prefix"
                parameters = {"prefix": current_prefix}
            else:
                capability = "echo"
                parameters = {}
            
            response = client.invoke_agent(user_input, capability, parameters)
            if response:
                print(f"Agent: {response}")
            else:
                print("Failed to get response from agent")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


@cli.command()
@click.pass_context
def health(ctx):
    """Check server health"""
    client = ctx.obj['client']
    
    if client.check_server_health():
        print("Server is healthy")
    else:
        print("Server is not reachable")


if __name__ == "__main__":
    cli()