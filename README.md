# Stardog Voicebox LangChain Integration

[![PyPI version](https://badge.fury.io/py/stardog-voicebox-langchain.svg)](https://badge.fury.io/py/stardog-voicebox-langchain)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

LangChain integration for Stardog Voicebox - enabling natural language querying of knowledge graphs through LangChain tools, runnables, and chains.

## Features

- **🔧 LangChain Tools**: Ready-to-use tools for LangChain agents
- **🔗 LCEL Runnables**: Composable runnables for building chains
- **🔄 Async & Sync**: Full support for both async and synchronous operations

## Installation

```bash
pip install stardog-voicebox-langchain-integration
```

For development:
```bash
git clone https://github.com/stardog-union/voicebox-langchain-integration.git
cd voicebox-langchain-integration-integration
make install-dev
```

## Quick Start

### Basic Usage with Tools

```python
from stardog_voicebox_langchain import VoiceboxClient, VoiceboxAskTool

# Initialize client
client = VoiceboxClient(api_token="your-voicebox-api-token")

# Create a tool
ask_tool = VoiceboxAskTool(client)

# Ask a question
result = await ask_tool._arun(question="What flights are delayed?")
print(result["answer"])
print(result["sparql_query"])
```

### Using with LangChain Agents

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from stardog_voicebox_langchain import VoiceboxClient, VoiceboxAskTool

# Set up Voicebox tools
client = VoiceboxClient(api_token="your-token")
tools = [VoiceboxAskTool(client)]

# Create an agent
llm = ChatOpenAI(model="gpt-4")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Run the agent
result = await agent_executor.ainvoke({
    "input": "Query the knowledge graph for delayed flights and summarize the results"
})
```

### Using Runnables in LCEL Chains

```python
from langchain_core.runnables import RunnablePassthrough
from stardog_voicebox_langchain import VoiceboxClient, VoiceboxAskRunnable

client = VoiceboxClient(api_token="your-token")

# Build a chain
chain = (
    RunnablePassthrough()
    | VoiceboxAskRunnable(client)
    | (lambda x: f"Answer: {x['answer']}")
)

# Execute the chain
result = await chain.ainvoke({"question": "Show me airports in Texas"})
```

## Architecture

The library provides three layers of abstraction:

### 1. Client Layer
`VoiceboxClient` - Core client for Stardog Voicebox API
- Handles authentication and connection management
- Provides async and sync methods
- Wraps `pystardog` library

### 2. Runnables Layer (Core)
LangChain `Runnable` implementations:
- `VoiceboxSettingsRunnable` - Retrieve app settings
- `VoiceboxAskRunnable` - Ask questions (with answers)
- `VoiceboxQueryRunnable` - Generate SPARQL queries

Runnables are the **core implementation** and support LCEL composition.

### 3. Tools Layer (Wrapper)
LangChain `BaseTool` implementations that wrap Runnables:
- `VoiceboxSettingsTool`
- `VoiceboxAskTool`
- `VoiceboxQueryTool`

Tools are designed for agent integration and follow the DRY principle by reusing Runnables internally.


## API Reference

### VoiceboxClient

```python
client = VoiceboxClient(
    api_token="your-token",           # Required: Voicebox API token
    client_id="my-app",                # Optional: Client identifier
    endpoint="https://...",            # Optional: API endpoint
    auth_token_override="sso-token"    # Optional: SSO auth token
)
```

**Methods:**
- `async_get_settings()` / `get_settings()` - Get Voicebox app settings
- `async_ask(question, conversation_id=None)` / `ask(...)` - Ask a question
- `async_generate_query(question, conversation_id=None)` / `generate_query(...)` - Generate SPARQL query

### VoiceboxAskRunnable

```python
runnable = VoiceboxAskRunnable(client)

# Async
result = await runnable.ainvoke({
    "question": "Your question here",
    "conversation_id": "optional-conv-id"
})

# Sync
result = runnable.invoke({...})
```

**Output:**
```python
{
    "answer": "Natural language answer",
    "sparql_query": "SELECT ...",
    "interpreted_question": "How Voicebox understood it",
    "conversation_id": "conv-123",
    "message_id": "msg-456"
}
```

### VoiceboxAskTool

```python
tool = VoiceboxAskTool(client)

# Async
result = await tool._arun(
    question="Your question",
    conversation_id="optional"
)

# Sync
result = tool._run(question="Your question")
```

## Examples

Check out the [`examples/`](examples/) directory for complete working examples:

- [`basic_tool_usage.py`](examples/basic_tool_usage.py) - Basic tool usage and multi-turn conversations
- [`agent_integration.py`](examples/agent_integration.py) - Integration with LangChain ReAct agents
- [`runnable_chains.py`](examples/runnable_chains.py) - LCEL chains and VoiceboxQAChain usage

Run an example:
```bash
export STARDOG_VOICEBOX_API_TOKEN="your-token"
export OPENAI_API_KEY="your-openai-key"  # For agent examples
python examples/basic_tool_usage.py
```

## Development

### Setup

```bash
# Install dependencies
make install-dev

# Run tests
make test

# Run tests with coverage
make test-cov

# Format code
make format

# Run all CI checks
make ci
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_client.py

# With coverage
pytest --cov=stardog_voicebox_langchain --cov-report=html
```

### Code Quality

```bash
# Format with black and isort
make format

# Type checking
make type-check

# Linting
make lint
```

## Configuration

### Environment Variables

The library respects the following environment variables:

- `STARDOG_VOICEBOX_API_TOKEN` - Voicebox API token
- `STARDOG_CLOUD_ENDPOINT` - Custom API endpoint (default: https://cloud.stardog.com/api)

### Getting Your API Token

1. Log in to [Stardog Cloud](https://cloud.stardog.com)
2. Navigate to your Voicebox application
3. Go to Settings → API Token
4. Copy your application API token

## Error Handling

The library provides custom exceptions for different error scenarios:

```python
from stardog_voicebox_langchain import (
    VoiceboxException,           # Base exception
    VoiceboxAuthenticationError, # Auth failures
    VoiceboxAPIError,            # API errors
    VoiceboxValidationError,     # Input validation errors
    VoiceboxConnectionError      # Connection failures
)

try:
    result = await client.async_ask("My question")
except VoiceboxAuthenticationError:
    print("Invalid API token")
except VoiceboxValidationError:
    print("Invalid input")
except VoiceboxAPIError as e:
    print(f"API error: {e.message}")
```

## How VoiceboxQAChain Works

The `VoiceboxQAChain` demonstrates how to build enhanced workflows on top of Voicebox:

### Simple Mode (No LLM)
```
User Question → VoiceboxAskRunnable → Answer + SPARQL Query
```

### Enhanced Mode (With LLM)
```
User Question → VoiceboxAskRunnable → (Answer, Query) → LLM Enhancement → Enhanced Answer
```

The chain shows:
1. **Composability**: Combines Voicebox with LLM post-processing
2. **Multi-turn Support**: Maintains conversation context
3. **Flexibility**: Can be used directly or converted to a Runnable for LCEL
4. **Optional Enhancement**: LLM can reformat/clarify answers while maintaining accuracy

Users can create their own custom chains following this pattern.


## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes, add tests and run `make test` to verify
4. Run `make ci` to verify
5. Submit a pull request


## General Support

- **Documentation**: [Stardog Documentation](https://docs.stardog.com/)
- **Community**: [Stardog Community](https://community.stardog.com/)

