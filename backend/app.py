import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from tempfile import NamedTemporaryFile

from src.job_recommender.agent.workflows.workflow import create_workflow

from src.job_recommender.core.exceptions_config import ProjectException
from src.job_recommender.core.logger_config import logger as log, log_api_call


api_app = FastAPI(title="Job Recommender API", version="0.1.0")
workflow_app = create_workflow()

@api_app.post('/process_resume', summary="Process a resume PDF and get recommendations")
async def process_resume(file: UploadFile = File(...)):


    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file.read())
            temp_filepath = temp_file.name
            log.info(f"processing file: {temp_filepath}")

            result = workflow_app.invoke({"filepath": temp_filepath})
            return {"status": "success", "result": result}
    except Exception as e:
        log.error(f"Error processing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")
    
    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
            log.info(f"Cleaned up temporary file: {temp_filepath}")
        