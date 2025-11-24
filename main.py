""" from src.job_recommender.demo.demo import test_pdf_loader, test_preprocess, test_vs, test_upsert_pipeline

test_upsert_pipeline() """

from src.job_recommender.workflow.automate import Automate
filepath = "C:/Users/asend/Downloads/resume_sample_student.pdf"
au = Automate(filepath=filepath)
au.auto()
