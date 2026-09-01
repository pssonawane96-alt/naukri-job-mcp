import os
import requests
from fastmcp import FastMCP

mcp = FastMCP("Job Finder")


@mcp.tool
def search_jobs(
    keyword: str,
    location: str = "",
    experience: str = ""
) -> dict:
    """
    Search Google Jobs through SerpApi and return real job listings.
    """

    api_key = os.environ.get("SERPAPI_KEY")

    if not api_key:
        return {
            "error": "SERPAPI_KEY is not configured in Render."
        }

    query = keyword

    if experience:
        query += f" {experience} years experience"

    params = {
        "engine": "google_jobs",
        "q": query,
        "api_key": api_key
    }

    if location:
        params["location"] = location

    try:
        response = requests.get(
            "https://serpapi.com/search.json",
            params=params,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        jobs = []

        for job in data.get("jobs_results", []):
            jobs.append({
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("location"),
                "description": job.get("description"),
                "posted_at": job.get("detected_extensions", {}).get("posted_at"),
                "job_url": job.get("share_link")
            })

        return {
            "query": query,
            "location": location,
            "experience": experience,
            "total_results": len(jobs),
            "jobs": jobs
        }

    except requests.RequestException as e:
        return {
            "error": f"Job search failed: {str(e)}"
        }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port
    )
