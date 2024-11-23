from .product_security_crew.security_requirement_crew import SecurityRequirementCrew
from .product_security_crew.threat_model_crew import ThreatModelCrew
from rag_management.query_embedding import similarity_search
from .general.general_crew import GeneralCrew
from knowledge_retrieval import util
import os
from dotenv import load_dotenv
load_dotenv()

temp_file = os.getenv('TEMP_FILE')
export_file = os.getenv('EXPORT_FILE')
detail_output_file = os.getenv('DETAILED_OUTPUT')

class MainCrew:
    def run(self, domain: str, task: str, prompt: str, image_path):
        util.remove_file(temp_file)
        util.remove_file(f"{export_file}.docx")
        util.remove_file(f"{export_file}.pdf")
        util.remove_file(detail_output_file)
    
        if(task == "Threat Modeling"):
            resp = ThreatModelCrew().run(system_information=prompt, image_path=image_path)
            return resp
        elif (task == "Security Requirements"):
            resp = SecurityRequirementCrew().run(system_information=prompt, image_path=image_path)
            return resp
        else:
            return "Not yet defined"

        
