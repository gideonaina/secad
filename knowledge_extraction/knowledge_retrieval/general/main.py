from knowledge_retrieval.kes_model import KESModel
import os

from dotenv import load_dotenv
load_dotenv()

openai_api_base = os.getenv('OPENAI_API_BASE')
openai_api_key = os.getenv('OPENAI_API_KEY')


class GeneralCrew:

  # def __init__(self, prompt):
  #   self.prompt = prompt
  #   self.llm = KESModel()


  def run(self, prompt):
    llm = KESModel().get_llm()
    response = llm.invoke(prompt)
    return response
