from apify_client import ApifyClient
from typing import List

from langchain_core.tools import tool

from src.job_recommender.core.api_key_config import api_key_config

from src.job_recommender.core.logger_config import logger as log
from src.job_recommender.core.exceptions_config import ProjectException

# @tool
def fetch_jobs_from_linkedin(query: List, location: str | None,  number_of_jobs: int = 20) -> List[dict]:
    """ extract job data from the linkedin using Apify API according to job keyword and location """

    try:
        apify_key = api_key_config.load()["APIFY_API_KEY"]
        apify_actor_id = api_key_config.load()["APIFY_ACTOR_ID"]
        log.info("APIFY API KEYS loaded...")
    except Exception as e:
        ProjectException(
            e, 
            context = {
                "operation": "Read APIFY API KEY"
            }
        )

    titles = f'"{", ".join(query)}"'
    if len(titles) == 0:
        log.warning("There are not titles passing to APIFY")


    try:
        apify_client = ApifyClient(apify_key)
        log.info("APIFY client created.")
        
        run_input = {
            "title": titles,
            "location": location if location else "",
            "rows": number_of_jobs,
        }
        log.info(f"Fetching jobs from LinkedIn, title: {titles[:100]}, location: {location}, num of jobs: {number_of_jobs}")

        run = apify_client.actor(apify_actor_id).call(run_input=run_input)
        linkedin_jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
        log.info(f"{len(linkedin_jobs)} LinkedIn jobs found.")
        return linkedin_jobs
    except Exception as e:
        ProjectException(
            e, 
            context = {
                "operation": "fetch jobs from linkedin"
            }
        )