from ddgs import DDGS
from ddgs.exceptions import DDGSException
from langchain.tools import tool
from .logger_handler import logging


@tool
def web_search(query: str) -> str:
    """Use this tool to search the internet for information."""
    logging.info("Performing web search for query: %s", query)

    try:
        results = DDGS(timeout=20).text(
            query,
            backend="auto",
            max_results=5,
        )

        if not results:
            logging.warning("No search results for: %s", query)
            return "No search results found."

        logging.info("Found %s search results", len(results))

        return "\n\n".join(
            f"Title: {result.get('title', '')}\n"
            f"URL: {result.get('href', '')}\n"
            f"Snippet: {result.get('body', '')}"
            for result in results
        )

    except DDGSException as error:
        logging.error("DuckDuckGo search failed: %s", error)
        return f"Web search unavailable: {error}"

    except Exception:
        logging.exception("Unexpected error during web search")
        return "Web search unavailable due to an unexpected error."
