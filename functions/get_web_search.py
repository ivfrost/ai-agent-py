import os
from tavily import TavilyClient
from config import WEB_MAX_RESULTS, WEB_MAX_QUERY_LEN
from typing import Literal

schema_get_web_search = {
    "name": "get_web_results",
    "description": "Search the web using Tavily to find relevant results for a query. Use for research, current events, or when the user needs information beyond your knowledge.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query optimized for accurate results, using correct terminology and no grammatical errors"
            },
            "time_range": {
                "type": "string",
                "description": "Optional time filter. Only set when the user explicitly requests recent results or when recency is clearly relevant. Accepted values: day, week, month, year"
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

def get_web_search(query: str, time_range: Literal["day", "week", "month", "year"] | None = None, topic: Literal["news", "finance"] | None = None, country: str | None = None) -> str:
    try:
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key:
            raise RuntimeError("TAVILY_API_KEY is not set")
        if len(query) > (WEB_MAX_QUERY_LEN or 30):
            raise ValueError(f"Query can't be longer than {WEB_MAX_QUERY_LEN}")
        tavily_client = TavilyClient(api_key=api_key)
        kwargs = {}
        if time_range:
            kwargs["time_range"] = time_range
        if topic:
            kwargs["topic"] = topic
        if country:
            kwargs["country"] = country
        results = tavily_client.search(query=query, max_results=WEB_MAX_RESULTS or 12, **kwargs).get("results", [])
        return "\n\n".join(
            f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content']}"
            for r in results
        )
    except Exception as e:
        if isinstance(e, (ValueError )):
            return (f"Error: {str(e)}")
        else:
            return (f"Error: Unexpected error ocurred")