"""Stardog Voicebox LangChain Integration.

This package provides LangChain integration for Stardog Voicebox, enabling
natural language querying over your enterprise data using LangChain runnables and tools.
"""

from .constants import (
    DEFAULT_CLIENT_ID,
    DEFAULT_STARDOG_CLOUD_ENDPOINT,
    ENV_CLOUD_ENDPOINT,
    ENV_VOICEBOX_API_TOKEN,
    ENV_VOICEBOX_CLIENT_ID,
)
from .exceptions import (
    VoiceboxAPIError,
    VoiceboxAuthenticationError,
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
    # Constants
    "DEFAULT_STARDOG_CLOUD_ENDPOINT",
    "DEFAULT_CLIENT_ID",
    "ENV_VOICEBOX_API_TOKEN",
    "ENV_VOICEBOX_CLIENT_ID",
    "ENV_CLOUD_ENDPOINT",
    # Version
    "__version__",
]
