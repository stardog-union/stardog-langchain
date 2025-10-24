"""Tests for Runnable implementations."""

import pytest

from stardog_voicebox_langchain import (
    VoiceboxAskRunnable,
    VoiceboxGenerateQueryRunnable,
    VoiceboxSettingsRunnable,
)


class TestVoiceboxSettingsRunnable:
    """Tests for VoiceboxSettingsRunnable."""

    @pytest.mark.asyncio
    async def test_ainvoke(self, voicebox_client):
        """Test async invocation of settings runnable."""
        runnable = VoiceboxSettingsRunnable(voicebox_client)
        result = await runnable.ainvoke({})

        assert result["name"] == "test-voicebox-app"
        assert result["database"] == "test-database"

    def test_invoke(self, voicebox_client):
        """Test sync invocation of settings runnable."""
        runnable = VoiceboxSettingsRunnable(voicebox_client)
        result = runnable.invoke({})

        assert result["name"] == "test-voicebox-app"
        assert result["database"] == "test-database"


class TestVoiceboxAskRunnable:
    """Tests for VoiceboxAskRunnable."""

    @pytest.mark.asyncio
    async def test_ainvoke(self, voicebox_client, sample_question):
        """Test async invocation of ask runnable."""
        runnable = VoiceboxAskRunnable(voicebox_client)
        result = await runnable.ainvoke({"question": sample_question})

        assert "answer" in result
        assert "sparql_query" in result
        assert "conversation_id" in result

    @pytest.mark.asyncio
    async def test_ainvoke_with_conversation_id(
        self, voicebox_client, sample_question, sample_conversation_id
    ):
        """Test async invocation with conversation_id."""
        runnable = VoiceboxAskRunnable(voicebox_client)
        result = await runnable.ainvoke(
            {"question": sample_question, "conversation_id": sample_conversation_id}
        )

        assert result is not None

    @pytest.mark.asyncio
    async def test_ainvoke_missing_question(self, voicebox_client):
        """Test that missing question raises ValueError."""
        runnable = VoiceboxAskRunnable(voicebox_client)
        with pytest.raises(ValueError, match="Input must contain a 'question' key"):
            await runnable.ainvoke({})

    def test_invoke(self, voicebox_client, sample_question):
        """Test sync invocation of ask runnable."""
        runnable = VoiceboxAskRunnable(voicebox_client)
        result = runnable.invoke({"question": sample_question})

        assert "answer" in result
        assert "sparql_query" in result

    def test_invoke_missing_question(self, voicebox_client):
        """Test that missing question raises ValueError in sync mode."""
        runnable = VoiceboxAskRunnable(voicebox_client)
        with pytest.raises(ValueError, match="Input must contain a 'question' key"):
            runnable.invoke({"wrong_key": "value"})


class TestVoiceboxQueryRunnable:
    """Tests for VoiceboxQueryRunnable."""

    @pytest.mark.asyncio
    async def test_ainvoke(self, voicebox_client, sample_question):
        """Test async invocation of query runnable."""
        runnable = VoiceboxGenerateQueryRunnable(voicebox_client)
        result = await runnable.ainvoke({"question": sample_question})

        assert "sparql_query" in result
        assert "interpreted_question" in result
        assert "conversation_id" in result

    @pytest.mark.asyncio
    async def test_ainvoke_with_conversation_id(
        self, voicebox_client, sample_question, sample_conversation_id
    ):
        """Test async invocation with conversation_id."""
        runnable = VoiceboxGenerateQueryRunnable(voicebox_client)
        result = await runnable.ainvoke(
            {"question": sample_question, "conversation_id": sample_conversation_id}
        )

        assert result is not None

    @pytest.mark.asyncio
    async def test_ainvoke_missing_question(self, voicebox_client):
        """Test that missing question raises ValueError."""
        runnable = VoiceboxGenerateQueryRunnable(voicebox_client)
        with pytest.raises(ValueError, match="Input must contain a 'question' key"):
            await runnable.ainvoke({})

    def test_invoke(self, voicebox_client, sample_question):
        """Test sync invocation of query runnable."""
        runnable = VoiceboxGenerateQueryRunnable(voicebox_client)
        result = runnable.invoke({"question": sample_question})

        assert "sparql_query" in result
        assert "interpreted_question" in result
