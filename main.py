
# from rec_system.graph.nodes.read_store_vec_store_node import read_store_vec_db
# from rec_system.utils import log, RecommendationSystemError
# from rec_system.client import load_llm_model
from rec_system.workflow.graph import app

def main():
    app.invoke({"original_filepath": "/mnt/e/Job-Recommender-System/sample_data/John Carter cv.pdf"})
    





if __name__ == "__main__":
    main()
