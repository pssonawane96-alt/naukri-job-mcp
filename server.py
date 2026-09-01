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
    Search for jobs matching the requested role, location and experience.

    This initial version prepares the job-search request.
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
        "message": "Naukri Job Finder is connected and ready for job-search integration."
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
