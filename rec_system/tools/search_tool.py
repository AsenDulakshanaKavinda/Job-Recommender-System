
import os
from langchain.tools import tool
from serpapi.google_search import GoogleSearch
from dotenv import load_dotenv; load_dotenv()
from rec_system.utils import log, RecommendationSystemError

key = os.getenv("SERP_API_KEY")


@tool
def find_online_courses(title: str):
    """ 
    Use the Google search and search for the online courses for the missing skills.
    args:
        title: str - title of the missing skills (use this to search on google).
    return:
        courses: dict - python dict of courses that found to learn the missing skills.
    """
    try:
        params = {
            "q": title,
            "hl": "en",
            "gl": "us",
            "device": "desktop",
            "api_key": key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        log.info(f"Finding courses for the: {title}")
        courses = results["organic_results"]
        return courses
    except Exception as e:
        RecommendationSystemError(
            e,
            context={
                "operation": "find online courses tool"
            }
        )


