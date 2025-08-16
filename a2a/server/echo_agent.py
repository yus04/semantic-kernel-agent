"""
Echo Agent implementation with invoke function
"""
import os
import yaml
from typing import Dict, Any
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from echo_plugin import EchoPlugin
from echo_agent_executor import EchoAgentExecutor


class EchoAgent:
    """
    Echo Agent using Semantic Kernel
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the Echo Agent
        
        Args:
            config_path: Path to the configuration file
        """
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # Substitute environment variables in config
        self._substitute_env_vars(self.config)
        
        # Initialize Semantic Kernel
        self.kernel = self._initialize_kernel()
        
        # Initialize executor
        self.executor = EchoAgentExecutor(self.kernel)
    
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
    
    async def invoke(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the agent with request data
        
        Args:
            request_data: The request data containing message, capability, and parameters
            
        Returns:
            The response from the agent
        """
        return await self.executor.execute(request_data)