# 1. testing pdf loader
from src.job_recommender.loaders.pdf_loader import PdfLoader

def test_pdf_loader(filepath) -> str:
    with open(filepath, 'rb') as file:
        loader = PdfLoader(file)
        text = loader.text_extractor()
        print("test pdf loader complited")
        return text

# 2. testing preprocess

from src.job_recommender.preprocessing.preprocessor import Preprocessor
def test_preprocess():
    filepath = "C:/Users/asend/Downloads/resume_sample_student.pdf"
    test_content = test_pdf_loader(filepath)
    preprocessr = Preprocessor(test_content)
    preprocess_content = preprocessr.preprocess()
    print("preprocessing complited")
    return preprocess_content

# 3. test model loader
from src.job_recommender.core.model_config import ModelConfig
def test_model_loader():
    ml = ModelConfig()
    ml.llm_model_loader()
    print("LLM Loaded")
    ml.embedding_model_loader()
    print("Embed Loaded")
    

# 3. test vs
from src.job_recommender.vector_db.langchain_vector_db_manager import LangchainVectorDBManager

def test_vs():
    test_chunks = test_preprocess()
    manager = LangchainVectorDBManager("test_session")
    manager.upsert(test_chunks)
    print("upsert done")
    manager.delete()
    print("namespace deleted")

