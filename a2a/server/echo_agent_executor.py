"""
Echo Agent Executor implementation using A2A SDK and Semantic Kernel
"""
from typing import Optional, Dict, Any
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.types import Message, TextPart, Role, TaskStatusUpdateEvent, TaskArtifactUpdateEvent, Artifact, TaskStatus, TaskState
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
            task_id = context.task_id
            context_id = getattr(context, 'context_id', task_id)
            
            # Extract text content from message parts
            text_content = ""
            for part in message.parts:
                if hasattr(part, 'text'):
                    text_content += part.text
                elif hasattr(part, 'root') and hasattr(part.root, 'text'):
                    text_content += part.root.text
            
            # Send status update - working
            working_status = TaskStatus(state=TaskState.working)
            working_event = TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=working_status,
                final=False
            )
            await event_queue.enqueue_event(working_event)
            
            # For now, just use the echo capability
            echo_function = self.kernel.get_function("echo_plugin", "echo")
            result = await echo_function.invoke(self.kernel, message=text_content)
            response_text = str(result)
            
            # Create response artifact
            response_artifact = Artifact(
                artifact_id=str(uuid.uuid4()),
                name="echo_response",
                description="Echo response",
                parts=[TextPart(text=response_text)]
            )
            
            # Send artifact update
            artifact_event = TaskArtifactUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                artifact=response_artifact,
                last_chunk=True
            )
            await event_queue.enqueue_event(artifact_event)
            
            # Send status update - completed
            completed_status = TaskStatus(state=TaskState.completed)
            completed_event = TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=completed_status,
                final=True
            )
            await event_queue.enqueue_event(completed_event)
            
        except Exception as e:
            # Send status update - failed
            failed_status = TaskStatus(state=TaskState.failed)
            failed_event = TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=getattr(context, 'context_id', task_id),
                status=failed_status,
                final=True,
                metadata={"error": str(e)}
            )
            await event_queue.enqueue_event(failed_event)
    
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