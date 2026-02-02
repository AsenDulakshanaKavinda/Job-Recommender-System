
# from rec_system.graph.nodes.read_store_vec_store_node import read_store_vec_db
from rec_system.utils import log, RecommendationSystem

def main():
    # read_store_vec_db()
    log.info("this is a test log.")
    try:
        return 10/0
    except Exception as e:
        RecommendationSystem(
            e,
            context={
                "operation": "main"
            }
        )


if __name__ == "__main__":
    main()
