import os
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

class KESModel:
    def get_llm(self) -> None:
      llm_url = os.getenv('OPENAI_API_BASE')

      #For local llm
      if (llm_url):
        return ChatOpenAI(
        model=os.getenv('OPENAI_MODEL_NAME'),
        base_url=os.getenv('OPENAI_API_BASE')
      ) 
      else:
        return ChatOpenAI(
        model=os.getenv('OPENAI_MODEL_NAME'),
        temperature=0.05
        )