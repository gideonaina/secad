import os
from crewai import Crew, Process
from rag_management.query_embedding import similarity_search
from knowledge_retrieval import utils
from dotenv import load_dotenv
load_dotenv()

temp_file = "/tmp/threat_model_crew_temp.md"
export_file = "/tmp/threat_model_crew_exported"
detail_output_file = "/tmp/crew_detail.md"

from .product_security_agents import ProductSecurityAgent
from .product_security_tasks import ProductSecurityTask

class ThreatModelCrew:
  def __init__(self):
      utils.remove_file(temp_file)
      utils.remove_file(f"{export_file}.docx")
      utils.remove_file(f"{export_file}.pdf")
      utils.remove_file(detail_output_file)

  def run(self, system_information, image_path, main_model, vision_model):
    agents = ProductSecurityAgent(main_model, vision_model)
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

    utils.append_to_file(detail_output_file, output.raw)

    trust_zone_identification_task = tasks.trust_boundary_identification_task(
      system_description=output.raw,
      agent=agents.trust_zone_identification_agent()
    )

    output = trust_zone_identification_task.execute_sync()
    utils.append_to_file(detail_output_file, output.raw)

    threat_scenario_task = tasks.threat_scenario_creation_task(
      system_description=output.raw,
      agent=agents.threat_scenario_agent()
    )

    output = threat_scenario_task.execute_sync()
    # rag_context = similarity_search(output.raw)
    utils.append_to_file(detail_output_file, output.raw)
    # util.append_to_file(detail_output_file, rag_context)

    control_measure_task = tasks.control_measure_task(
      system_description=output.raw,
      agent=agents.controls_agent()
    )
    output = control_measure_task.execute_sync()
    utils.append_to_file(detail_output_file, output.raw)
    utils.append_to_file(temp_file, output.raw)

    return output.raw

    
    # trust_zone_output = trust_zone_identification_task.output

    # crew = Crew(
    #   agents=[
    #     architectural_analysis_agent, trust_zone_identification_agent
    #   ],
    #   tasks=[architectural_analysis_task, trust_zone_identification_task],
    #   verbose=True,
    #   process=Process.sequential
    # )

    # result = crew.kickoff()
    # util.append_to_temp_file(result)
    # return f"""
    #   # analysis_output.raw
    #   {result}
    # """
    # return result

    # for task in crew.tasks:
    #   output = task.execute_sync()
    #   util.append_to_temp_file(output.raw)
