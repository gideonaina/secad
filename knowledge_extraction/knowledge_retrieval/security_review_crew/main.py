import os
from crewai import Crew, Process
from knowledge_retrieval import util
from dotenv import load_dotenv
load_dotenv()

openai_api_base = os.getenv('OPENAI_API_BASE')
openai_api_key = os.getenv('OPENAI_API_KEY')
temp_file = os.getenv('TEMP_FILE')
detail_output_file = os.getenv('DETAILED_OUTPUT')


# print(f"OPENAI_API_BASE: {openai_api_base}")
# print(f"OPENAI_API_KEY: {openai_api_key}")

# if not openai_api_base:
#     raise KeyError("OPENAI_API_BASE environment variable is not set")

# if not openai_api_key:
#     raise KeyError("OPENAI_API_KEY environment variable is not set")


from .security_review_agents import SecurityReviewAgent
from .security_review_tasks import SecurityReviewTasks

class SecurityReviewCrew:

  # def __init__(self, system_information):
  #   self.system_information = system_information

  def run(self, system_information, image_path):
    agents = SecurityReviewAgent()
    tasks = SecurityReviewTasks()

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
    util.append_to_file(detail_output_file, output.raw)

    control_measure_task = tasks.control_measure_task(
      system_description=output.raw,
      agent=agents.controls_agent()
    )

    output = control_measure_task.execute_sync()
    util.append_to_file(detail_output_file, output.raw)
    util.append_to_file(temp_file, output.raw)

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
