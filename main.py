from src.job_recommender.agent.workflows.workflow import create_workflow

filepath = "C:/Users/asend/Desktop/fake_resume.pdf"

app = create_workflow()
result = app.invoke({"filepath": filepath})
from pprint import pprint

pprint(result)

""" from src.job_recommender.agent.tools.read_content import read_content

read_content()
 """
print("+---"* 20)
print("+---"* 20)
