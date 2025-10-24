"""Basic example demonstrating Voicebox Tools usage.

This example shows how to use Voicebox tools directly for simple
question-answering tasks.
"""

import asyncio
import os

from stardog_voicebox_langchain import (
    VoiceboxAskTool,
    VoiceboxClient,
    VoiceboxGenerateQueryTool,
)


async def main():
    """Main example function."""
    # Initialize the client with your API token
    # You can get this from your Stardog Cloud Voicebox app settings
    api_token = os.getenv("STARDOG_VOICEBOX_API_TOKEN")
    if not api_token:
        print("Please set STARDOG_VOICEBOX_API_TOKEN environment variable")
        return

    client = VoiceboxClient(
        api_token=api_token,
        client_id="example-client",  # Optional: identify your application
    )

    # Create tools
    ask_tool = VoiceboxAskTool(client)
    query_tool = VoiceboxGenerateQueryTool(client)

    print("=== Voicebox Tools Example ===\n")

    # Example 1: Ask a question and get an answer
    print("Example 1: Asking a question")
    question = "What flights are delayed?"
    result = await ask_tool._arun(question=question)

    print(f"Question: {question}")
    print(f"Answer: {result['answer']}")
    print(f"SPARQL Query: {result['sparql_query']}")
    print(f"Conversation ID: {result['conversation_id']}\n")

    # Example 2: Generate a query without executing it
    print("Example 2: Generating a SPARQL query")
    question2 = "Show me all airports in California"
    query_result = await query_tool._arun(question=question2)

    print(f"Question: {question2}")
    print(f"Generated Query: {query_result['sparql_query']}")
    print(f"Interpreted as: {query_result['interpreted_question']}\n")

    # Example 3: Multi-turn conversation
    print("Example 3: Multi-turn conversation")
    first_question = "What flights depart from SFO?"
    first_result = await ask_tool._arun(question=first_question)

    print(f"Question 1: {first_question}")
    print(f"Answer 1: {first_result['answer']}\n")

    # Use the conversation_id for follow-up
    conversation_id = first_result["conversation_id"]
    followup_question = "Which of those are going to New York?"
    followup_result = await ask_tool._arun(
        question=followup_question, conversation_id=conversation_id
    )

    print(f"Question 2: {followup_question}")
    print(f"Answer 2: {followup_result['answer']}\n")

    print("=== Example Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
