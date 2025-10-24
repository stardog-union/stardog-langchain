"""Example demonstrating Voicebox tools integration with LangChain agents.

This example shows how to use Voicebox tools with a LangChain ReAct agent
to enable the agent to query a knowledge graph.
"""

import asyncio
import os

# Note: This example requires langchain and an LLM provider
# Install with: pip install langchain langchain-openai
try:
    from langchain.agents import AgentExecutor, create_react_agent
    from langchain_core.prompts import PromptTemplate
    from langchain_openai import ChatOpenAI
except ImportError:
    print("This example requires langchain and langchain-openai:")
    print("pip install langchain langchain-openai")
    exit(1)

from stardog_voicebox_langchain import (
    VoiceboxAskTool,
    VoiceboxClient,
    VoiceboxSettingsTool,
)


async def main():
    """Main example function."""
    # Check for required environment variables
    voicebox_token = os.getenv("STARDOG_VOICEBOX_API_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not voicebox_token:
        print("Please set STARDOG_VOICEBOX_API_TOKEN environment variable")
        return
    if not openai_key:
        print("Please set OPENAI_API_KEY environment variable")
        return

    # Initialize Voicebox client
    client = VoiceboxClient(api_token=voicebox_token)

    # Create Voicebox tools
    tools = [
        VoiceboxSettingsTool(client),
        VoiceboxAskTool(client),
    ]

    # Initialize LLM (using OpenAI GPT-4 as an example)
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Create a ReAct agent with Voicebox tools
    prompt = PromptTemplate.from_template(
        """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
    )

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
    )

    print("=== Voicebox Agent Example ===\n")

    # Example 1: Simple question
    print("Example 1: Simple knowledge graph query")
    result1 = await agent_executor.ainvoke(
        {"input": "What can you tell me about the Voicebox application settings?"}
    )
    print(f"Result: {result1['output']}\n")

    # Example 2: Complex multi-step reasoning
    print("\nExample 2: Multi-step reasoning with Voicebox")
    result2 = await agent_executor.ainvoke(
        {
            "input": "First, find out what flights are delayed. Then, tell me which of those flights "
            "are international flights."
        }
    )
    print(f"Result: {result2['output']}\n")

    # Example 3: Combining Voicebox with agent reasoning
    print("\nExample 3: Agent reasoning with Voicebox data")
    result3 = await agent_executor.ainvoke(
        {
            "input": "Query the knowledge graph for all airports, and then tell me how many "
            "there are and suggest the top 3 busiest ones."
        }
    )
    print(f"Result: {result3['output']}\n")

    print("=== Example Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
