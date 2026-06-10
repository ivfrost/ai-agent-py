import os
from tavily import TavilyClient
from config import WEB_MAX_RESULTS, WEB_MAX_QUERY_LEN
from typing import Literal

schema_get_web_content = {
    "name": "get_web_content",
    "description": "Being provided a set of relevant URLs, extract the main content from each URL and return it as a structured string.",
    "input_schema": {
        "type": "object",
        "properties": {
            "urls": {
                "type": "array",
                "description": "List of URLs to extract content from",
                "items": {
                    "type": "string"
                },
            },
            "extract_depth": {
                "type": "string",
                "description": "Level of content extraction detail. 'basic' for simple text extraction, 'advanced' for more comprehensive extraction including tables, structured data, media",
                "enum": ["basic", "advanced"]
            },
            "query": {
                "type": "string",
                "description": "Optional original user query that prompted the content extraction. Providing this can help the extraction process focus on relevant information related to the query."
            }
        },
        "required": ["urls"]
    }
}


def get_web_content(urls: list[str], extract_depth: Literal['basic', 'advanced'] | None = None, query: str | None = None) -> str:
    try:
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key:
            raise RuntimeError("TAVILY_API_KEY is not set")
        tavily_client = TavilyClient(api_key=api_key)
        kwargs = {}
        if extract_depth:
            kwargs["extract_depth"] = extract_depth
        if query:
            kwargs["query"] = query
          
        response = tavily_client.extract(urls=urls, **kwargs)
        return "\n\n".join(
            f"URL: {r['url']}\nContent: {r.get('raw_content') or 'No content extracted'}"
            for r in response.get("results", [])
        )
    except Exception as e:
        if isinstance(e, (ValueError )):
            return (f"Error: {str(e)}")
        else:
            return (f"Error: Unexpected error ocurred")