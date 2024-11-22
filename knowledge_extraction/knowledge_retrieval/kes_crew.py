from .security_review_crew.main import SecurityReviewCrew
from rag_management.query_embedding import similarity_search
from .general.main import GeneralCrew
from knowledge_retrieval import util
import os
from dotenv import load_dotenv
load_dotenv()

temp_file = os.getenv('TEMP_FILE')
export_file = os.getenv('EXPORT_FILE')
detail_output_file = os.getenv('DETAILED_OUTPUT')

class KESCrew:
    def run(self, domain: str, task: str, prompt: str, image_path):
        util.remove_file(temp_file)
        util.remove_file(f"{export_file}.docx")
        util.remove_file(f"{export_file}.pdf")
        util.remove_file(detail_output_file)

        '''
        Task - determine the crew to run
        Domain - determine the RAG data to use (i.e similarity search scope)
        '''
        # resp = SecurityReviewCrew().run(system_information=prompt, image_path=image_path)
        # return resp
    
        if(task == "Threat Modeling"):
            resp = SecurityReviewCrew().run(system_information=prompt, image_path=image_path)
            return resp
        elif (task == "Security Requirements"):
            resp = SecurityReviewCrew().run(system_information=prompt, image_path=image_path)
            return resp
        else:
            return "Not yet defined"

        
