
import os
from typing import List
from pydantic import BaseModel, Field
from langchain.tools import tool
from serpapi.google_search import GoogleSearch
from dotenv import load_dotenv; load_dotenv()
from rec_system.utils import log, RecommendationSystemError

key = os.getenv("SERP_API_KEY")

class CourseOutput(BaseModel):
    title: str = Field(description="Title of the course.")
    link: str = Field(description="Link to the course website.")
    snippet: str  = Field(description="Simple description of the course.")
    source: str = Field(description="Website or organization conducting the course.")

class SearchToolOutput(BaseModel):
    search_output: dict


@tool
def find_online_courses(skill_title: str):

    """ 
    tool: find_online_courses

    description: 
        Use the Google search and search for the online courses for the missing skills.
    args:
        skill_title: str - title of the missing skills (use this to search on google).
    return:
        courses: dict - python dict of courses that found to learn the missing skills.
    """
    try:
        params = {
            "q": skill_title,
            "hl": "en",
            "gl": "us",
            "device": "desktop",
            "api_key": key
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        log.info(f"Finding courses for the: {skill_title}")

        courses: List[CourseOutput] = []

        for item in results.get("organic_results", []):
            course = CourseOutput(
                title=item.get("title", "Unknown course"),
                link=item.get("link", ""),
                snippet=item.get("snippet", ""),
                source=item.get("source", "Unknown")
            )
            courses.append(course)
        
        return {"courses": courses}

    except Exception as e:
        RecommendationSystemError(
            e,
            context={
                "operation": "find online courses tool"
            }
        )


