from typing import Any, Optional

from langchain_core.runnables import Runnable, RunnableConfig

from .voicebox_client import VoiceboxClient


class VoiceboxSettingsRunnable(Runnable[dict[str, Any], dict[str, Any]]):
    """Runnable for retrieving Voicebox application settings.

    This runnable retrieves the configuration and metadata for a Voicebox application.
    It can be composed with other runnables in LangChain chains.

    Args:
        client: VoiceboxClient instance

    Example:
        >>> client = VoiceboxClient(api_token="your-token")
        >>> runnable = VoiceboxSettingsRunnable(client)
        >>> settings = await runnable.ainvoke({})
        >>> print(settings["database"])
    """

    def __init__(self, client: VoiceboxClient) -> None:
        """Initialize the runnable with a Voicebox client."""
        super().__init__()
        self.client = client

    def invoke(
        self,
        input: dict[str, Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Synchronously retrieve Voicebox settings.

        Args:
            input: Input dictionary (ignored, can be empty)
            config: Optional runtime configuration
            **kwargs: Additional keyword arguments

        Returns:
            Dictionary containing Voicebox application settings
        """
        return self.client.get_settings()

    async def ainvoke(
        self,
        input: dict[str, Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Asynchronously retrieve Voicebox settings.

        Args:
            input: Input dictionary (ignored, can be empty)
            config: Optional runtime configuration
            **kwargs: Additional keyword arguments

        Returns:
            Dictionary containing Voicebox application settings
        """
        return await self.client.async_get_settings()


class VoiceboxAskRunnable(Runnable[dict[str, Any], dict[str, Any]]):
    """Runnable for asking questions to Voicebox.

    This runnable asks natural language questions and receives AI-generated answers
    from Stardog Voicebox. It supports multi-turn conversations via conversation_id.

    Args:
        client: VoiceboxClient instance

    Example:
        >>> client = VoiceboxClient(api_token="your-token")
        >>> runnable = VoiceboxAskRunnable(client)
        >>> result = await runnable.ainvoke({"question": "What flights are delayed?"})
        >>> print(result["answer"])
    """

    def __init__(self, client: VoiceboxClient) -> None:
        """Initialize the runnable with a Voicebox client."""
        super().__init__()
        self.client = client

    def invoke(
        self,
        input: dict[str, Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Synchronously ask a question to Voicebox.

        Args:
            input: Dictionary containing:
                - question (required): Natural language question
                - conversation_id (optional): Conversation ID for context
            config: Optional runtime configuration
            **kwargs: Additional keyword arguments

        Returns:
            Dictionary containing answer, query, and conversation metadata
        """
        question = input.get("question")
        if not question:
            raise ValueError("Input must contain a 'question' key")

        conversation_id = input.get("conversation_id")
        return self.client.ask(question=question, conversation_id=conversation_id)

    async def ainvoke(
        self,
        input: dict[str, Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Asynchronously ask a question to Voicebox.

        Args:
            input: Dictionary containing:
                - question (required): Natural language question
                - conversation_id (optional): Conversation ID for context
            config: Optional runtime configuration
            **kwargs: Additional keyword arguments

        Returns:
            Dictionary containing answer, query, and conversation metadata
        """
        question = input.get("question")
        if not question:
            raise ValueError("Input must contain a 'question' key")

        conversation_id = input.get("conversation_id")
        return await self.client.async_ask(
            question=question, conversation_id=conversation_id
        )


class VoiceboxGenerateQueryRunnable(Runnable[dict[str, Any], dict[str, Any]]):
    """Runnable for generating SPARQL queries from natural language.

    This runnable generates SPARQL queries from natural language questions
    without executing them. Useful for query inspection or custom execution.

    Args:
        client: VoiceboxClient instance

    Example:
        >>> client = VoiceboxClient(api_token="your-token")
        >>> runnable = VoiceboxGenerateQueryRunnable(client)
        >>> result = await runnable.ainvoke({"question": "Show me all airports"})
        >>> print(result["sparql_query"])
    """

    def __init__(self, client: VoiceboxClient) -> None:
        """Initialize the runnable with a Voicebox client."""
        super().__init__()
        self.client = client

    def invoke(
        self,
        input: dict[str, Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Synchronously generate a SPARQL query.

        Args:
            input: Dictionary containing:
                - question (required): Natural language question
                - conversation_id (optional): Conversation ID for context
            config: Optional runtime configuration
            **kwargs: Additional keyword arguments

        Returns:
            Dictionary containing generated query and metadata
        """
        question = input.get("question")
        if not question:
            raise ValueError("Input must contain a 'question' key")

        conversation_id = input.get("conversation_id")
        return self.client.generate_query(
            question=question, conversation_id=conversation_id
        )

    async def ainvoke(
        self,
        input: dict[str, Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Asynchronously generate a SPARQL query.

        Args:
            input: Dictionary containing:
                - question (required): Natural language question
                - conversation_id (optional): Conversation ID for context
            config: Optional runtime configuration
            **kwargs: Additional keyword arguments

        Returns:
            Dictionary containing generated query and metadata
        """
        question = input.get("question")
        if not question:
            raise ValueError("Input must contain a 'question' key")

        conversation_id = input.get("conversation_id")
        return await self.client.async_generate_query(
            question=question, conversation_id=conversation_id
        )
