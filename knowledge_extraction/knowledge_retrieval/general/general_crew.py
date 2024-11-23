from knowledge_retrieval.llm_model import LLMModel
import os

from dotenv import load_dotenv
load_dotenv()

openai_api_base = os.getenv('OPENAI_API_BASE')
openai_api_key = os.getenv('OPENAI_API_KEY')


class GeneralCrew:
  
  def run(self, prompt):
    llm = LLMModel().get_llm()
    response = llm.invoke(prompt)
    return response
