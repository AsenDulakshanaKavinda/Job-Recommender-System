
import uuid
from datetime import datetime

from langchain_core.messages import HumanMessage, ToolMessage, BaseMessage, SystemMessage

from src.job_recommender.pipeline.data_upsert_pipeline import DataUpsert
from src.job_recommender.agent.graph import build_rag_agent 

from src.job_recommender.core.exceptions_config import ProjectException
from src.job_recommender.core.logger_config import logger as log

def generate_session_id() -> str:
    """"
    generate a unique session ID based on the current timestamp
    and random 8-character uuid format
    eg:-
        session_20250115_153045_a1b2c3d4
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid.uuid4().hex[:8]
    return f"session_{timestamp}_{unique_id}"

class Automate:
    def __init__(self, filepath: str, session_id: str = None):
        self.filepath = filepath
        self.session_id = session_id or generate_session_id()

    def auto(self):
        self.automate_upsert(self.filepath, self.session_id)
        self.automate_rag_agent()
        

    def automate_upsert(self, filepath: str, session_id: str):
        try:
            data_upsert = DataUpsert(filepath, session_id)
            data_upsert.upsert_pipeline()
            log.info(f"Data upsert completed....")
        except Exception as e:
            log.error(f"Error while Automating the upsert")  
            ProjectException(
                e,
                context = {
                    "operation": f"automate_upsert",
                    "value": "Error while Automating the upsert"
                },
                reraise=True
            )

    def automate_rag_agent(self):
        rag = build_rag_agent(self.session_id)
        self._resume_summery(rag)


    def _resume_summery(self, rag_agent):
        summery_query = "Generate a summery of the entire resume document."
        summery_message = [HumanMessage(content=summery_query)]
        summery_payload = {'messages': summery_message}
        summery_result = rag_agent.invoke(summery_payload)
        print("Generated summery: ")
        print(summery_result['messages'][-1].content)





