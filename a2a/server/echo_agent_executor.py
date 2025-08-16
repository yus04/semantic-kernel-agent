"""
Echo Agent Executor implementation using A2A SDK and Semantic Kernel
"""
from typing import Optional, Dict, Any
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.utils.message import MessageToDict
from a2a.types import Message, TextPart, Role
from semantic_kernel import Kernel
import uuid

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
        
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        Execute the agent request
        
        Args:
            context: The request context containing the message and metadata
            event_queue: Event queue for publishing results
        """
        try:
            # Get the message from the context
            message = context.message
            
            # Extract text content from message parts
            text_content = ""
            for part in message.parts:
                if hasattr(part, 'text'):
                    text_content += part.text
                elif hasattr(part, 'root') and hasattr(part.root, 'text'):
                    text_content += part.root.text
            
            # For now, just use the echo capability
            echo_function = self.kernel.get_function("echo_plugin", "echo")
            result = await echo_function.invoke(self.kernel, message=text_content)
            response_text = str(result)
            
            # Create response message
            response_message = Message(
                message_id=str(uuid.uuid4()),
                role=Role.agent,
                parts=[TextPart(text=response_text)]
            )
            
            # Convert to dict for event queue
            response_dict = MessageToDict(response_message)
            
            # Send response through event queue
            await event_queue.put({
                "type": "message",
                "message": response_dict
            })
            
        except Exception as e:
            # Send error through event queue
            await event_queue.put({
                "type": "error",
                "error": f"Error executing agent request: {str(e)}"
            })
    
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