import os
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

class KESModel:
    def get_llm(self) -> None:
      return ChatOpenAI(
        model=os.getenv('OPENAI_MODEL_NAME'),
        base_url=os.getenv('OPENAI_API_BASE'),
        temperature=os.getenv('MODEL_TEMP')
      )