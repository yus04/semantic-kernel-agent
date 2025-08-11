"""
EchoPlugin for Semantic Kernel
Simple plugin that echoes back the input message
"""
from typing import Annotated
from semantic_kernel.functions import kernel_function


class EchoPlugin:
    """
    A simple echo plugin that returns the same message it receives.
    """

    @kernel_function(
        name="echo",
        description="Echoes back the input message",
    )
    def echo(
        self,
        message: Annotated[str, "The message to echo back"]
    ) -> str:
        """
        Echo the input message back to the caller.
        
        Args:
            message: The message to echo back
            
        Returns:
            The same message that was input
        """
        return message

    @kernel_function(
        name="echo_with_prefix",
        description="Echoes back the input message with a prefix",
    )
    def echo_with_prefix(
        self,
        message: Annotated[str, "The message to echo back"],
        prefix: Annotated[str, "Prefix to add to the message"] = "Echo: "
    ) -> str:
        """
        Echo the input message back with a prefix.
        
        Args:
            message: The message to echo back
            prefix: The prefix to add (defaults to "Echo: ")
            
        Returns:
            The message with prefix
        """
        return f"{prefix}{message}"