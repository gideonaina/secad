import os
from crewai import Crew, Process
from rag_management.query_embedding import similarity_search
from knowledge_retrieval import util
from dotenv import load_dotenv
load_dotenv()

openai_api_base = os.getenv('OPENAI_API_BASE')
openai_api_key = os.getenv('OPENAI_API_KEY')
temp_file = os.getenv('TEMP_FILE')
detail_output_file = os.getenv('DETAILED_OUTPUT')


from .product_security_agents import ProductSecurityAgent
from .product_security_tasks import ProductSecurityTask

class SecurityRequirementCrew:

  def run(self, system_information, image_path):
    agents = ProductSecurityAgent()
    tasks = ProductSecurityTask()

    if(image_path):
      arch_diagram_information = tasks.architecture_image_analysis_task(
        image_path= image_path,
        agent=agents.system_information_agent()
      )
      output = arch_diagram_information.execute_sync()

    elif (system_information):
      architectural_analysis_task = tasks.anaylsis_task(
        system_description=system_information,
        agent=agents.architectural_analysis_agent()
      )
      output = architectural_analysis_task.execute_sync()

    else:
      return "Input information required"

    util.append_to_file(detail_output_file, output.raw)

    trust_zone_identification_task = tasks.trust_boundary_identification_task(
      system_description=output.raw,
      agent=agents.trust_zone_identification_agent()
    )

    output = trust_zone_identification_task.execute_sync()
    util.append_to_file(detail_output_file, output.raw)

    threat_scenario_task = tasks.threat_scenario_creation_task(
      system_description=output.raw,
      agent=agents.threat_scenario_agent()
    )

    output = threat_scenario_task.execute_sync()
    # rag_context = similarity_search(output.raw)
    util.append_to_file(detail_output_file, output.raw)

    requirement_task = tasks.requirement_generation_task(
      system_description=output.raw,
      agent=agents.requirement_agent()
    )

    output = requirement_task.execute_sync()

    util.append_to_file(detail_output_file, output.raw)
    util.append_to_file(temp_file, output.raw)

    return util.json_to_security_requirement_table(output.raw)
