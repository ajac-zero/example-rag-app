"""`agent.py` defines the Agent class, which is the main logic abstraction for the application.

The main objective of the Agent class is to provide instructions to the AI through the system prompt and tool definitions,
along with access to components from the 'components' module in order to perform actions as needed.

An Agent instance uses components configured and provided by the 'config' module. It also imports the 'types' module for type-hinting.

The Agent class is what the entrypoints must import to interact with the application logic.
"""

from __future__ import annotations

import json

from . import config, types

__all__ = ["Agent"]


SYSTEM_PROMPT = """
You are a helpful assistant that can use a search engine to answer user's questions.

There are three types of searches you can perform:

1. Semantic search:
This search uses semantic similarity to find content that is similar to the query.
Semantic search is best used when you need to retrieve content based on meaning rather than exact words.
It excels in handling synonyms, context, and intent.
It should generally be used when you want information that might be phrased differently to the query.

2. Keyword search:
This search uses keyword search to find content that contain all the keywords in the list.
Keyword search is best used when precision and exact matches are required. Especially for structured and technical queries.
It excels in handlings terms, abbreviations, and speficic phrases.
It should generally be used when you know the exact terms you are looking for.

3. Hybrid search:
This search combines both semantic and keyword search.
Hybrid search is best when you need both relevance and precision.
It combines semantic search's ability to understand meaning with keyword search's ability to find exact matches.
It should generally be used when you expect specific terms while also wanting contextually relevant results.

You must determine when each type of search is appropriate for a given query.
If the user does not ask a question, you may answer without performing a search.
""".strip()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "hybrid_search",
            "description": "Query the search engine for relevant documents using both semantic and keyword search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query that will be converted to an embedding and used in semantic search.",
                    },
                    "keywords": {
                        "type": "array",
                        "description": "Relevant keywords to narrow down the search with BM25 search.",
                        "items": {"type": "string"},
                    },
                },
                "required": ["query", "keywords"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "semantic_search",
            "description": "Query the search engine for relevant documents using semantic similarity search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query that will be converted to an embedding and used in semantic search.",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "keyword_search",
            "description": "Query the search engine for relevant documents using keyword search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "array",
                        "description": "Relevant keywords to narrow down the search with BM25 search.",
                        "items": {"type": "string"},
                    },
                },
                "required": ["keywords"],
            },
        },
    },
]


class Agent:
    """`Agent` encapsulates a system prompt, tool definitions, and tool execution logic."""

    system = SYSTEM_PROMPT
    tools = TOOLS

    def __init__(
        self,
        model: str,
        embedding_model: str | None = None,
        _inference: types.InferenceProtocol | None = None,
        _search: types.SearchProtocol | None = None,
    ) -> None:
        """Initialize an `Agent` instance.

        Args:
            model (str): The model to use for inference, as defined in the litellm config.
            embedding_model (str, optional): The model to use for embedding generation. Defaults to "text-embedding-3-large".
            _inference (InferenceProtocol, optional): The inference component to use to generate embeddings and chat completions.
            _search (SearchProtocol, optional): The search component to use to generate search results.

        """
        self.model = model
        self.embedding_model = embedding_model or "text-embedding-3-large"
        self.inference = _inference or config.get_openai()
        self.search = _search or config.get_qdrant()

        self.tool_map = {
            "hybrid_search": self._hybrid_search_pipeline,
            "semantic_search": self._semantic_search_pipeline,
            "keyword_search": self._keyword_search_pipeline,
        }

    async def _hybrid_search_pipeline(
        self, query: str, keywords: list[str], limit: int = 25
    ):
        """Pipeline to perform a hybrid search and build a string template."""
        query_embedding = await self.inference.generate_embedding(
            text=query, model=self.embedding_model
        )

        search_results = await self.search.hybrid_search(
            query=query_embedding, keywords=keywords, limit=limit
        )

        template = self._build_template(search_results)

        return template

    async def _semantic_search_pipeline(self, query: str, limit: int = 25):
        """Pipeline to perform a semantic search and build a string template."""
        query_embedding = await self.inference.generate_embedding(
            text=query, model=self.embedding_model
        )

        search_results = await self.search.semantic_search(
            query=query_embedding, limit=limit
        )

        template = self._build_template(search_results)

        return template

    async def _keyword_search_pipeline(self, keywords: list[str], limit: int = 25):
        """Pipeline to perform a keyword search and build a string template."""
        search_results = await self.search.keyword_search(
            keywords=keywords, limit=limit
        )

        template = self._build_template(search_results)

        return template

    def _build_template(self, result: list[types.SearchResult]) -> str:
        """Use the results of a search to build a string template."""
        return "\n".join(
            [
                "<CONTENT>\n{content}\n</CONTENT>".format(
                    content=search["data"]["content"]
                )
                for search in result
            ]
        )

    async def execute(self, tool_name: str, *args, **kwargs):
        """Fetch a tool function from the agent's tool map and runs it given the arguments.

        Args:
            tool_name (str): The name of the tool to execute as listed in the agent's tool map.
            *args: Variable-length argument list to pass to the tool function.
            **kwargs: Arbitrary keyword arguments to pass to the tool function.

        Returns:
            The given tool function's return value.

        """
        return await self.tool_map[tool_name](*args, **kwargs)  # type: ignore[operator]

    async def generate(
        self, messages: types.Messages, **kwargs
    ) -> types.AsyncGenerator[str, None]:
        """Send messages to the LLM to generate a response.

        If the LLM responds with a tool call, execute the tool and
        append the result to the messages list.

        Args:
            messages (Messages): The list of messages to send to the LLM. Each message
                is a dictionary with a "role" key and a "content" key.  The "role" key
                can be "user" or "assistant", and the "content" key is the message
                to send to the LLM.
            **kwargs: Arbitrary keyword arguments to pass to the LLM.

        Returns:
            An asynchronous generator that yields the LLM's response content one token (str) at a time.

        """
        assistant_message: types.AssistantMessage = {"role": "assistant"}
        messages.append(assistant_message)

        async for chunk in self.inference.generate_stream(
            messages[:-1], model=self.model, tools=self.tools, **kwargs
        ):
            if content := chunk["content"]:
                if "content" not in assistant_message:
                    assistant_message["content"] = ""

                assistant_message["content"] += content
                yield content

            if tools := chunk["tools"]:
                assistant_message["tool_calls"] = tools

                for tool in tools:
                    result = await self.execute(
                        tool_name=tool["function"]["name"],
                        **json.loads(tool["function"]["arguments"]),
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool["id"],
                            "content": result,
                        }
                    )

                async for content in self.generate(messages):
                    yield content
