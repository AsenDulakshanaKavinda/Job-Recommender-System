


from job_recommender.src.loaders.pdf_loader import PdfLoader
from job_recommender.src.preprocessing.preprocessor import Preprocessor

test_file = "C:/Users/asend\Downloads/resume_sample_student.pdf"
def test_pdf_loader():
    with open(test_file, 'rb') as f:
        loader = PdfLoader(f)
        text = loader.text_extractor()
        print(text)
        return text

content = test_pdf_loader()

pr = Preprocessor(content=content)
cl = pr.preprocess()
print(cl)
