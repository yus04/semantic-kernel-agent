"""
Echo Agent Executor implementation using A2A SDK and Semantic Kernel
"""
from typing import Optional, Dict, Any
from a2a.server.agent_execution.agent_executor import AgentExecutor
from semantic_kernel import Kernel

from echo_plugin import EchoPlugin


class EchoAgentExecutor(AgentExecutor):
    """
    Agent Executor for Echo Agent using Semantic Kernel
    """
    
    def __init__(self, kernel: Kernel):
        """
        Initialize the Echo Agent Executor
        
        Args:
            kernel: The Semantic Kernel instance
        """
        self.kernel = kernel
        
    async def execute(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent request
        
        Args:
            request_data: The request data containing message, capability, and parameters
            
        Returns:
            The response from the agent execution
        """
        try:
            message = request_data.get("message", "")
            capability = request_data.get("capability", "echo")
            parameters = request_data.get("parameters", {})
            
            if capability == "echo":
                echo_function = self.kernel.get_function("echo_plugin", "echo")
                result = await echo_function.invoke(self.kernel, message=message)
                response_text = str(result)
                
            elif capability == "echo_with_prefix":
                echo_function = self.kernel.get_function("echo_plugin", "echo_with_prefix")
                prefix = parameters.get("prefix", "Echo: ")
                result = await echo_function.invoke(
                    self.kernel, 
                    message=message,
                    prefix=prefix
                )
                response_text = str(result)
                
            else:
                raise ValueError(f"Unsupported capability: {capability}")
                
            return {
                "response": response_text,
                "agent_id": "echo-agent-v1",
                "capability_used": capability
            }
            
        except Exception as e:
            raise Exception(f"Error executing agent request: {str(e)}")
    
    async def cancel(self, task_id: str) -> bool:
        """
        Cancel a running task
        
        Args:
            task_id: The ID of the task to cancel
            
        Returns:
            True if cancellation was successful, False otherwise
        """
        # For the echo agent, we don't have long-running tasks to cancel
        # This is a simple implementation that always returns True
        return True