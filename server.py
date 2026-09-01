import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Naukri Job Finder",
    json_response=True
)


@mcp.tool()
def search_jobs(
    keyword: str,
    location: str = "",
    experience: str = ""
) -> dict:
    """
    Search for jobs matching role, location and experience.
    """

    search_query = keyword

    if location:
        search_query += f" {location}"

    if experience:
        search_query += f" {experience}"

    return {
        "status": "ready",
        "job_role": keyword,
        "location": location,
        "experience": experience,
        "search_query": search_query,
        "message": "Naukri Job Finder is connected and ready."
    }


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
