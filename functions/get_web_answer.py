import os
from tavily import TavilyClient
from config import WEB_MAX_RESULTS, WEB_MAX_QUERY_LEN
from typing import Literal

schema_get_web_answer = {
    "name": "get_web_answer",
    "description": "Search the web to get a direct answer to a simple factual question.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query optimized for accurate results, using correct terminology and no grammatical errors"
            },
            "topic": {
                "type": "string",
                "description": "Optional topic filter. Only set when the query is clearly about news or finance. Accepted values: news, finance"
            },
            "country": {
                "type": "string",
                "description": "Optional country code. Set when location context is relevant, inferred from the query or user language"
            }
        },
        "required": ["query"]
    }
}

def get_web_answer(query: str, topic: Literal["news", "finance"] | None = None, country: str | None = None) -> str:
    try:
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key:
            raise RuntimeError("TAVILY_API_KEY is not set")
        if len(query) > (WEB_MAX_QUERY_LEN or 30):
            raise ValueError(f"Query can't be longer than {WEB_MAX_QUERY_LEN}")
        tavily_client = TavilyClient(api_key=api_key)
        kwargs = {}
        if topic:
            kwargs["topic"] = topic
        if country:
            kwargs["country"] = country
        return tavily_client.qna_search(
          query=query,
          max_results=WEB_MAX_RESULTS or 12,
          **kwargs
        )
        
    except Exception as e:
        if isinstance(e, (ValueError )):
            return (f"Error: {str(e)}")
        else:
            return (f"Error: Unexpected error ocurred")