"""Example demonstrating Voicebox Runnables and Chains usage.

This example shows how to use Voicebox runnables in LangChain Expression Language (LCEL)
chains and the pre-built VoiceboxQAChain.
"""

import asyncio
import os

from langchain_core.runnables import RunnablePassthrough

from stardog_voicebox_langchain import (
    VoiceboxAskRunnable,
    VoiceboxClient,
    VoiceboxGenerateQueryRunnable,
)


async def example_basic_runnable():
    """Example 1: Basic runnable usage."""
    print("=== Example 1: Basic Runnable ===\n")

    api_token = os.getenv("STARDOG_VOICEBOX_API_TOKEN")
    client = VoiceboxClient(api_token=api_token)

    # Create a runnable
    ask_runnable = VoiceboxAskRunnable(client)

    # Use it directly
    result = await ask_runnable.ainvoke({"question": "What flights are delayed?"})

    print(f"Answer: {result['answer']}")
    print(f"Query: {result['sparql_query']}\n")


async def example_lcel_chain():
    """Example 2: Composing runnables with LCEL."""
    print("=== Example 2: LCEL Chain Composition ===\n")

    api_token = os.getenv("STARDOG_VOICEBOX_API_TOKEN")
    client = VoiceboxClient(api_token=api_token)

    # Build a chain: input -> Voicebox -> extract answer
    chain = (
        RunnablePassthrough()
        | VoiceboxAskRunnable(client)
        | (lambda x: f"Answer: {x['answer']}\n\nQuery used: {x['sparql_query']}")
    )

    result = await chain.ainvoke({"question": "Show me airports in Texas"})
    print(result)
    print()


async def example_query_generation_chain():
    """Example 3: Query generation chain."""
    print("=== Example 3: Query Generation Chain ===\n")

    api_token = os.getenv("STARDOG_VOICEBOX_API_TOKEN")
    client = VoiceboxClient(api_token=api_token)

    # Create a chain that generates queries from natural language
    query_chain = VoiceboxGenerateQueryRunnable(client) | (lambda x: x["sparql_query"])

    questions = [
        "What flights depart from SFO?",
        "Show me all airlines",
        "Which flights are delayed?",
    ]

    for question in questions:
        query = await query_chain.ainvoke({"question": question})
        print(f"Question: {question}")
        print(f"Generated Query: {query}\n")


async def main():
    """Run all examples."""
    api_token = os.getenv("STARDOG_VOICEBOX_API_TOKEN")
    if not api_token:
        print("Please set STARDOG_VOICEBOX_API_TOKEN environment variable")
        return

    await example_basic_runnable()
    await example_lcel_chain()
    await example_query_generation_chain()

    print("=== All Examples Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
