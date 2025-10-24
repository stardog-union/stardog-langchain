"""Tests for Tool implementations."""

import pytest

from stardog_voicebox_langchain import (
    VoiceboxAskTool,
    VoiceboxGenerateQueryTool,
    VoiceboxSettingsTool,
)


class TestVoiceboxSettingsTool:
    """Tests for VoiceboxSettingsTool."""

    def test_tool_metadata(self, voicebox_client):
        """Test tool has correct metadata."""
        tool = VoiceboxSettingsTool(voicebox_client)

        assert tool.name == "voicebox_settings"
        assert "Voicebox application settings" in tool.description

    def test_run(self, voicebox_client):
        """Test synchronous tool execution."""
        tool = VoiceboxSettingsTool(voicebox_client)
        result = tool._run()

        assert result["name"] == "test-voicebox-app"
        assert result["database"] == "test-database"

    @pytest.mark.asyncio
    async def test_arun(self, voicebox_client):
        """Test asynchronous tool execution."""
        tool = VoiceboxSettingsTool(voicebox_client)
        result = await tool._arun()

        assert result["name"] == "test-voicebox-app"
        assert result["database"] == "test-database"


class TestVoiceboxAskTool:
    """Tests for VoiceboxAskTool."""

    def test_tool_metadata(self, voicebox_client):
        """Test tool has correct metadata."""
        tool = VoiceboxAskTool(voicebox_client)

        assert tool.name == "voicebox_ask"
        assert "natural language question" in tool.description.lower()
        assert tool.args_schema is not None

    def test_run(self, voicebox_client, sample_question):
        """Test synchronous tool execution."""
        tool = VoiceboxAskTool(voicebox_client)
        result = tool._run(question=sample_question)

        assert "answer" in result
        assert "sparql_query" in result
        assert "conversation_id" in result

    def test_run_with_conversation_id(
        self, voicebox_client, sample_question, sample_conversation_id
    ):
        """Test synchronous tool execution with conversation_id."""
        tool = VoiceboxAskTool(voicebox_client)
        result = tool._run(
            question=sample_question, conversation_id=sample_conversation_id
        )

        assert result is not None

    @pytest.mark.asyncio
    async def test_arun(self, voicebox_client, sample_question):
        """Test asynchronous tool execution."""
        tool = VoiceboxAskTool(voicebox_client)
        result = await tool._arun(question=sample_question)

        assert "answer" in result
        assert "sparql_query" in result

    @pytest.mark.asyncio
    async def test_arun_with_conversation_id(
        self, voicebox_client, sample_question, sample_conversation_id
    ):
        """Test asynchronous tool execution with conversation_id."""
        tool = VoiceboxAskTool(voicebox_client)
        result = await tool._arun(
            question=sample_question, conversation_id=sample_conversation_id
        )

        assert result is not None

    def test_tool_schema_validation(self, voicebox_client):
        """Test tool input schema validation."""
        tool = VoiceboxAskTool(voicebox_client)
        schema = tool.args_schema

        # Check that question field is required
        assert "question" in schema.model_fields
        assert schema.model_fields["question"].is_required()


class TestVoiceboxQueryTool:
    """Tests for VoiceboxQueryTool."""

    def test_tool_metadata(self, voicebox_client):
        """Test tool has correct metadata."""
        tool = VoiceboxGenerateQueryTool(voicebox_client)

        assert tool.name == "voicebox_generate_query"
        assert "SPARQL query" in tool.description
        assert tool.args_schema is not None

    def test_run(self, voicebox_client, sample_question):
        """Test synchronous tool execution."""
        tool = VoiceboxGenerateQueryTool(voicebox_client)
        result = tool._run(question=sample_question)

        assert "sparql_query" in result
        assert "interpreted_question" in result

    def test_run_with_conversation_id(
        self, voicebox_client, sample_question, sample_conversation_id
    ):
        """Test synchronous tool execution with conversation_id."""
        tool = VoiceboxGenerateQueryTool(voicebox_client)
        result = tool._run(
            question=sample_question, conversation_id=sample_conversation_id
        )

        assert result is not None

    @pytest.mark.asyncio
    async def test_arun(self, voicebox_client, sample_question):
        """Test asynchronous tool execution."""
        tool = VoiceboxGenerateQueryTool(voicebox_client)
        result = await tool._arun(question=sample_question)

        assert "sparql_query" in result
        assert "interpreted_question" in result

    @pytest.mark.asyncio
    async def test_arun_with_conversation_id(
        self, voicebox_client, sample_question, sample_conversation_id
    ):
        """Test asynchronous tool execution with conversation_id."""
        tool = VoiceboxGenerateQueryTool(voicebox_client)
        result = await tool._arun(
            question=sample_question, conversation_id=sample_conversation_id
        )

        assert result is not None
