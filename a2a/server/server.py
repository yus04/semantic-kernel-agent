"""
A2A Echo Agent Server using Semantic Kernel and FastAPI
"""
import os
import yaml
import argparse
from typing import Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Load Semantic Kernel components
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# Local imports
from echo_plugin import EchoPlugin
from agent_card import AgentCard


class MessageRequest(BaseModel):
    """Request model for agent invocation"""
    message: str
    capability: str = "echo"
    parameters: Dict[str, Any] = {}


class MessageResponse(BaseModel):
    """Response model for agent invocation"""
    response: str
    agent_id: str
    capability_used: str


class EchoAgentServer:
    """
    Echo Agent Server using Semantic Kernel
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # Substitute environment variables in config
        self._substitute_env_vars(self.config)
        
        # Initialize Semantic Kernel
        self.kernel = self._initialize_kernel()
        
        # Initialize FastAPI app
        self.app = FastAPI(
            title="A2A Echo Agent",
            description="Echo Agent using Semantic Kernel for A2A communication",
            version="1.0.0"
        )
        
        # Setup routes
        self._setup_routes()
        
        # Create agent card
        self.agent_card = AgentCard.create_echo_agent_card()

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

    def _initialize_kernel(self) -> Kernel:
        """Initialize Semantic Kernel with Azure OpenAI"""
        kernel = Kernel()
        
        # Add Azure OpenAI service
        azure_openai_config = self.config["azure_openai"]
        
        chat_completion = AzureChatCompletion(
            deployment_name=azure_openai_config["deployment_name"],
            endpoint=azure_openai_config["endpoint"],
            api_key=azure_openai_config["api_key"],
            api_version=azure_openai_config["api_version"]
        )
        
        kernel.add_service(chat_completion)
        
        # Add Echo Plugin
        echo_plugin = EchoPlugin()
        kernel.add_plugin(echo_plugin, plugin_name="echo_plugin")
        
        return kernel

    def _setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.get("/")
        async def root():
            return {"message": "A2A Echo Agent Server", "status": "running"}
        
        @self.app.get("/agent/card")
        async def get_agent_card():
            """Get the AgentCard for this agent"""
            return self.agent_card.model_dump()
        
        @self.app.post("/agent/invoke", response_model=MessageResponse)
        async def invoke_agent(request: MessageRequest):
            """Invoke the agent with a message"""
            try:
                # Use the Echo Plugin directly for simple echo
                if request.capability == "echo":
                    echo_function = self.kernel.get_function("echo_plugin", "echo")
                    result = await echo_function.invoke(self.kernel, message=request.message)
                    response_text = str(result)
                    
                elif request.capability == "echo_with_prefix":
                    echo_function = self.kernel.get_function("echo_plugin", "echo_with_prefix")
                    prefix = request.parameters.get("prefix", "Echo: ")
                    result = await echo_function.invoke(
                        self.kernel, 
                        message=request.message,
                        prefix=prefix
                    )
                    response_text = str(result)
                    
                else:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Unsupported capability: {request.capability}"
                    )
                
                return MessageResponse(
                    response=response_text,
                    agent_id=self.agent_card.agent_id,
                    capability_used=request.capability
                )
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {"status": "healthy", "agent": self.agent_card.name}

    def run(self, host: str = None, port: int = None):
        """Run the server"""
        server_config = self.config.get("server", {})
        host = host or server_config.get("host", "localhost")
        port = port or server_config.get("port", 8000)
        
        # Ensure port is an integer (from environment variables, it comes as string)
        if isinstance(port, str):
            try:
                port = int(port)
            except ValueError:
                print(f"Warning: Invalid port value '{port}', using default 8000")
                port = 8000

        print(f"Starting A2A Echo Agent Server on {host}:{port}")
        print(f"Agent Card available at: http://{host}:{port}/agent/card")
        print(f"Invoke endpoint: http://{host}:{port}/agent/invoke")
        
        uvicorn.run(
            self.app,
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