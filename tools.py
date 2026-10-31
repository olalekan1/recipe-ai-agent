
from langchain.tools import tool
from ddgs import DDGS
from ddgs.exceptions import DDGSException
from logger_handler import logging


@tool
def web_search(query: str) -> str:
    """Use this tool to search the internet for information."""

    logging.info(f"Performing web search for query: {query}")

    try:
        results = DDGS(timeout=20).text(
            query,
            backend="auto",
            max_results=5
        )

        if not results:
            logging.warning(f"No search results for: {query}")
            return "No search results found."

        logging.info(f"Found {len(results)} search results")

        return "\n\n".join(
            f"Title: {result.get('title', '')}\n"
            f"URL: {result.get('href', '')}\n"
            f"Snippet: {result.get('body', '')}"
            for result in results
        )

    except DDGSException as e:
        logging.error(f"DuckDuckGo search failed: {e}")
        return f"Web search unavailable: {e}"

    except Exception:
        logging.exception("Unexpected error during web search")
        return "Web search unavailable due to an unexpected error."
