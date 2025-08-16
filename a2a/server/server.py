"""
A2A Echo Agent Server using Semantic Kernel and A2A SDK
"""
import argparse
import uvicorn
from a2a.server.apps.jsonrpc.starlette_app import A2AStarletteApplication
from a2a.server.request_handlers.default_request_handler import DefaultRequestHandler
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.types import AgentCard

# Local imports
from echo_agent import EchoAgent


def create_agent_card() -> AgentCard:
    """
    Create an AgentCard for the Echo Agent using A2A types
    
    Returns:
        AgentCard instance for the Echo Agent
    """
    from a2a.types import AgentSkill, AgentCapabilities
    
    # Create skills for the echo agent
    echo_skill = AgentSkill(
        id="echo",
        name="echo",
        description="Echoes back the input message",
        input_modes=["text"],
        output_modes=["text"],
        examples=["Hello World!"],
        tags=["echo", "simple"]
    )
    
    echo_with_prefix_skill = AgentSkill(
        id="echo_with_prefix",
        name="echo_with_prefix", 
        description="Echoes back the input message with a prefix",
        input_modes=["text"],
        output_modes=["text"],
        examples=["Hello World! with prefix"],
        tags=["echo", "prefix"]
    )
    
    # Create capabilities
    capabilities = AgentCapabilities(
        streaming=False,
        push_notifications=False,
        state_transition_history=False
    )
    
    return AgentCard(
        name="EchoAgent",
        description="An echo agent that returns the same message it receives using Semantic Kernel",
        version="1.0.0",
        url="http://localhost:8000",
        skills=[echo_skill, echo_with_prefix_skill],
        capabilities=capabilities,
        default_input_modes=["text"],
        default_output_modes=["text"]
    )


class EchoAgentServer:
    """
    Echo Agent Server using A2A SDK and Semantic Kernel
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the Echo Agent Server
        
        Args:
            config_path: Path to the configuration file
        """
        # Initialize the agent
        self.agent = EchoAgent(config_path)
        
        # Create agent card
        self.agent_card = create_agent_card()
        
        # Create task store
        self.task_store = InMemoryTaskStore()
        
        # Create request handler with agent executor
        self.request_handler = DefaultRequestHandler(
            agent_executor=self.agent.executor,
            task_store=self.task_store
        )
        
        # Create A2A Starlette application
        self.app = A2AStarletteApplication(
            agent_card=self.agent_card,
            http_handler=self.request_handler
        )
    
    def run(self, host: str = None, port: int = None):
        """Run the server"""
        # Load config for server settings
        import yaml
        with open("config.yaml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Substitute environment variables
        self.agent._substitute_env_vars(config)
        
        server_config = config.get("server", {})
        host = host or server_config.get("host", "localhost")
        port = port or server_config.get("port", 8000)
        
        # Ensure port is an integer
        if isinstance(port, str):
            try:
                port = int(port)
            except ValueError:
                print(f"Warning: Invalid port value '{port}', using default 8000")
                port = 8000

        print(f"Starting A2A Echo Agent Server on {host}:{port}")
        print(f"Agent Card available at: http://{host}:{port}/.well-known/agent-card.json")
        print(f"Invoke endpoint: http://{host}:{port}/")
        
        # Build the actual Starlette app
        starlette_app = self.app.build()
        
        uvicorn.run(
            starlette_app,
            host=host,
            port=port,
            log_level="info"
        )


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="A2A Echo Agent Server")
    parser.add_argument("--host", default=None, help="Host to bind to")
    parser.add_argument("--port", type=int, default=None, help="Port to bind to")
    parser.add_argument("--config", default="config.yaml", help="Configuration file path")
    
    args = parser.parse_args()
    
    # Initialize and run server
    server = EchoAgentServer(config_path=args.config)
    server.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()