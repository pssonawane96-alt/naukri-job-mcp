from mcp.server.fastmcp import FastMCP
import os
import urllib.parse
import requests

mcp = FastMCP(
    "Naukri Job Finder",
    json_response=True
)


@mcp.tool()
def search_jobs(
    keyword: str,
    location: str = "",
    experience: str = "",
    max_results: int = 10
) -> dict:
    """
    Search for publicly available Naukri job listings.

    Args:
        keyword: Job title or skills, e.g. Mainframe Developer COBOL JCL
        location: Preferred location, e.g. Pune or Mumbai
        experience: Experience range, e.g. 4-6 years
        max_results: Maximum number of results to return
    """

    query_parts = [
        f"site:naukri.com/job-listings {keyword}"
    ]

    if location:
        query_parts.append(location)

    if experience:
        query_parts.append(f'"{experience}"')

    query = " ".join(query_parts)

    # Use Google/Bing-style public search endpoint configured by deployment.
    search_url = os.getenv("SEARCH_URL")

    if not search_url:
        return {
            "status": "setup_required",
            "message": (
                "Search provider is not configured yet. "
                "The MCP server is working, but SEARCH_URL must be configured "
                "before job results can be returned."
            ),
            "search_query": query
        }

    try:
        encoded_query = urllib.parse.quote_plus(query)

        url = search_url.replace("{query}", encoded_query)

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get("results", [])[:max_results]:
            results.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("description")
            })

        return {
            "status": "success",
            "query": query,
            "results": results
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
