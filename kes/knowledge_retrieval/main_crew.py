import os

from dotenv import load_dotenv

from knowledge_retrieval import utils

from .product_security_crew.security_requirement_crew import SecurityRequirementCrew
from .product_security_crew.threat_model_crew import ThreatModelCrew

load_dotenv()

temp_file = os.getenv('TEMP_FILE')
export_file = os.getenv('EXPORT_FILE')
detail_output_file = os.getenv('DETAILED_OUTPUT')

class MainCrew:
    def run(self, main_model, vision_model, task: str, prompt: str, image_path):
        utils.remove_file(temp_file)
        utils.remove_file(f"{export_file}.docx")
        utils.remove_file(f"{export_file}.pdf")
        utils.remove_file(detail_output_file)
    
        if(task == "Threat Modeling"):
            resp = ThreatModelCrew().run(system_information=prompt, image_path=image_path, main_model=main_model, vision_model=vision_model)
            return resp
        elif (task == "Security Requirements"):
            resp = SecurityRequirementCrew().run(system_information=prompt, image_path=image_path, main_model=main_model, vision_model=vision_model)
            return resp
        else:
            return "Not yet defined"

        
