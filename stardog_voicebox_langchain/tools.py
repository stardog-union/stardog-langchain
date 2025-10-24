from typing import Any, Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from .runnables import (
    VoiceboxAskRunnable,
    VoiceboxGenerateQueryRunnable,
    VoiceboxSettingsRunnable,
)
from .voicebox_client import VoiceboxClient


# Input schemas for tools
class VoiceboxSettingsInput(BaseModel):
    """Input schema for VoiceboxSettingsTool (no inputs required)."""

    pass


class VoiceboxAskInput(BaseModel):
    """Input schema for VoiceboxAskTool."""

    question: str = Field(description="Natural language question to ask Voicebox")
    conversation_id: Optional[str] = Field(
        default=None,
        description="Optional conversation ID for multi-turn conversations",
    )


class VoiceboxGenerateQueryInput(BaseModel):
    """Input schema for VoiceboxQueryTool."""

    question: str = Field(
        description="Natural language question to convert to a SPARQL query"
    )
    conversation_id: Optional[str] = Field(
        default=None, description="Optional conversation ID for context"
    )


class VoiceboxSettingsTool(BaseTool):
    """Tool for retrieving Voicebox application settings.

    This tool retrieves the configuration and metadata for a Voicebox application.
    It can be used in LangChain agents to understand the available data sources.

    Args:
        client: VoiceboxClient instance

    Example:
        >>> client = VoiceboxClient(api_token="your-token")
        >>> tool = VoiceboxSettingsTool(client)
        >>> result = tool.invoke({})
    """

    name: str = "voicebox_settings"
    description: str = (
        "Retrieve Voicebox application settings including database name, "
        "model name, named graphs, and reasoning configuration. "
        "Use this to understand what data sources are available."
    )
    args_schema: Type[BaseModel] = VoiceboxSettingsInput

    client: VoiceboxClient
    runnable: VoiceboxSettingsRunnable

    def __init__(self, client: VoiceboxClient, **kwargs: Any) -> None:
        """Initialize the tool with a Voicebox client."""
        runnable = VoiceboxSettingsRunnable(client)
        super().__init__(client=client, runnable=runnable, **kwargs)

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict[str, Any]:
        """Execute the tool synchronously."""
        return self.runnable.invoke({})

    async def _arun(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict[str, Any]:
        """Execute the tool asynchronously."""
        return await self.runnable.ainvoke({})


class VoiceboxAskTool(BaseTool):
    """Tool for asking questions to Voicebox.

    This tool asks natural language questions and receives AI-generated answers
    from Stardog Voicebox. It's ideal for question-answering tasks in agents.

    Args:
        client: VoiceboxClient instance

    Example:
        >>> client = VoiceboxClient(api_token="your-token")
        >>> tool = VoiceboxAskTool(client)
        >>> result = tool.invoke({"question": "What flights are delayed?"})
    """

    name: str = "voicebox_ask"
    description: str = (
        "Ask a natural language question to Stardog Voicebox and get an answer. "
        "This tool queries the knowledge graph and returns a natural language answer "
        "along with the generated SPARQL query. Supports multi-turn conversations "
        "by passing conversation_id."
    )
    args_schema: Type[BaseModel] = VoiceboxAskInput

    client: VoiceboxClient
    runnable: VoiceboxAskRunnable

    def __init__(self, client: VoiceboxClient, **kwargs: Any) -> None:
        """Initialize the tool with a Voicebox client."""
        runnable = VoiceboxAskRunnable(client)
        super().__init__(client=client, runnable=runnable, **kwargs)

    def _run(
        self,
        question: str,
        conversation_id: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict[str, Any]:
        """Execute the tool synchronously."""
        return self.runnable.invoke(
            {"question": question, "conversation_id": conversation_id}
        )

    async def _arun(
        self,
        question: str,
        conversation_id: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict[str, Any]:
        """Execute the tool asynchronously."""
        return await self.runnable.ainvoke(
            {"question": question, "conversation_id": conversation_id}
        )


class VoiceboxGenerateQueryTool(BaseTool):
    """Tool for generating SPARQL queries from natural language.

    This tool generates SPARQL queries from natural language questions
    without executing them. Useful when you want to inspect or modify
    queries before execution.

    Args:
        client: VoiceboxClient instance

    Example:
        >>> client = VoiceboxClient(api_token="your-token")
        >>> tool = VoiceboxGenerateQueryTool(client)
        >>> result = tool.invoke({"question": "Show me all airports"})
    """

    name: str = "voicebox_generate_query"
    description: str = (
        "Generate a SPARQL query from a natural language question without executing it. "
        "This is useful when you want to see the query that would be generated "
        "or when you want to execute it yourself with custom parameters."
    )
    args_schema: Type[BaseModel] = VoiceboxGenerateQueryInput

    client: VoiceboxClient
    runnable: VoiceboxGenerateQueryRunnable

    def __init__(self, client: VoiceboxClient, **kwargs: Any) -> None:
        """Initialize the tool with a Voicebox client."""
        runnable = VoiceboxGenerateQueryRunnable(client)
        super().__init__(client=client, runnable=runnable, **kwargs)

    def _run(
        self,
        question: str,
        conversation_id: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict[str, Any]:
        """Execute the tool synchronously."""
        return self.runnable.invoke(
            {"question": question, "conversation_id": conversation_id}
        )

    async def _arun(
        self,
        question: str,
        conversation_id: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict[str, Any]:
        """Execute the tool asynchronously."""
        return await self.runnable.ainvoke(
            {"question": question, "conversation_id": conversation_id}
        )
