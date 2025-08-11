"""
AgentCard implementation for A2A Echo Agent
"""
from typing import Dict, Any, List
from pydantic import BaseModel


class AgentCapability(BaseModel):
    """Represents a capability of the agent"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


class AgentCard(BaseModel):
    """
    AgentCard representing the Echo Agent's capabilities and metadata
    """
    agent_id: str
    name: str
    description: str
    version: str
    capabilities: List[AgentCapability]
    metadata: Dict[str, Any]

    @classmethod
    def create_echo_agent_card(cls) -> "AgentCard":
        """
        Create an AgentCard for the Echo Agent
        
        Returns:
            AgentCard instance for the Echo Agent
        """
        capabilities = [
            AgentCapability(
                name="echo",
                description="Echoes back the input message",
                input_schema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message to echo back"
                        }
                    },
                    "required": ["message"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "response": {
                            "type": "string",
                            "description": "The echoed message"
                        }
                    }
                }
            ),
            AgentCapability(
                name="echo_with_prefix",
                description="Echoes back the input message with a prefix",
                input_schema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message to echo back"
                        },
                        "prefix": {
                            "type": "string",
                            "description": "Prefix to add to the message",
                            "default": "Echo: "
                        }
                    },
                    "required": ["message"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "response": {
                            "type": "string",
                            "description": "The echoed message with prefix"
                        }
                    }
                }
            )
        ]

        return cls(
            agent_id="echo-agent-v1",
            name="EchoAgent",
            description="An echo agent that returns the same message it receives using Semantic Kernel",
            version="1.0.0",
            capabilities=capabilities,
            metadata={
                "framework": "semantic-kernel",
                "author": "A2A Sample Implementation",
                "tags": ["echo", "sample", "semantic-kernel"],
                "endpoint": "/agent/invoke"
            }
        )