import os
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

class KESModel:
    def get_llm(self):
      return ChatOpenAI(
        model=os.getenv('OPENAI_MODEL_NAME'),
        base_url=os.getenv('OPENAI_API_BASE'),
        temperature=os.getenv('MODEL_TEMP')
      )
    
    def get_vision_model(self):
      return ChatOpenAI(
        model=os.getenv('VISION_MODEL'),
        base_url=os.getenv('OPENAI_API_BASE'),
        temperature=os.getenv('MODEL_TEMP')
      )