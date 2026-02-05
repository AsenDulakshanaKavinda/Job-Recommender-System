
# from rec_system.graph.nodes.read_store_vec_store_node import read_store_vec_db
# from rec_system.utils import log, RecommendationSystemError
# from rec_system.client import load_llm_model
# from rec_system.workflow.graph import app

from serpapi.google_search import GoogleSearch
import os
from dotenv import load_dotenv; load_dotenv()
# = os.getenv["SERP_API_KEY"]


def test():
    params = {
    "q": "machine learning online course",
    "hl": "en",
    "gl": "us",
    "device": "desktop",
    "api_key": "f7b88d650e5a9b5a38163daa0317a8ed90497e4de2109c15cc59296dbc0793b8"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    # courses = results["courses"]
    print(results)

def main():
    # app.invoke({"original_filepath": "/mnt/e/Job-Recommender-System/sample_data/John Carter cv.pdf"})
    test()





if __name__ == "__main__":
    main()
