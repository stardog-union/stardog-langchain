"""Stardog Voicebox LangChain Integration.

This package provides LangChain integration for Stardog Voicebox, enabling
natural language querying of knowledge graphs through LangChain tools,
runnables, and chains.

Quick Start:
    >>> from stardog_voicebox_langchain import VoiceboxClient, VoiceboxAskTool
    >>> client = VoiceboxClient(api_token="your-token")
    >>> tool = VoiceboxAskTool(client)
    >>> result = tool.invoke({"question": "What flights are delayed?"})

Components:
    - VoiceboxClient: Client for connecting to Stardog Voicebox API
    - Runnables: VoiceboxSettingsRunnable, VoiceboxAskRunnable, VoiceboxQueryRunnable
    - Tools: VoiceboxSettingsTool, VoiceboxAskTool, VoiceboxQueryTool
"""

from .constants import DEFAULT_CLIENT_ID, DEFAULT_STARDOG_CLOUD_ENDPOINT, Headers
from .exceptions import (
    VoiceboxAPIError,
    VoiceboxAuthenticationError,
    VoiceboxConnectionError,
    VoiceboxException,
    VoiceboxValidationError,
)
from .runnables import (
    VoiceboxAskRunnable,
    VoiceboxGenerateQueryRunnable,
    VoiceboxSettingsRunnable,
)
from .tools import VoiceboxAskTool, VoiceboxGenerateQueryTool, VoiceboxSettingsTool
from .voicebox_client import VoiceboxClient

__version__ = "0.1.0"

__all__ = [
    # Client
    "VoiceboxClient",
    # Runnables
    "VoiceboxSettingsRunnable",
    "VoiceboxAskRunnable",
    "VoiceboxGenerateQueryRunnable",
    # Tools
    "VoiceboxSettingsTool",
    "VoiceboxAskTool",
    "VoiceboxGenerateQueryTool",
    # Exceptions
    "VoiceboxException",
    "VoiceboxAuthenticationError",
    "VoiceboxAPIError",
    "VoiceboxValidationError",
    "VoiceboxConnectionError",
    # Constants
    "DEFAULT_STARDOG_CLOUD_ENDPOINT",
    "DEFAULT_CLIENT_ID",
    "Headers",
    # Version
    "__version__",
]
