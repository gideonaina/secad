from dotenv import load_dotenv

from knowledge_retrieval import utils
from knowledge_retrieval.product_security_crew.product_security_agents import (
  ProductSecurityAgent,
)
from knowledge_retrieval.product_security_crew.product_security_tasks import (
  ProductSecurityTask,
)

load_dotenv()

temp_file = "/tmp/threat_model_crew_temp.md"
export_file = "/tmp/threat_model_crew_exported"
detail_output_file = "/tmp/crew_detail.md"



class RequirementRefinementCrew:
  def __init__(self):
      utils.remove_file(temp_file)
      utils.remove_file(f"{export_file}.docx")
      utils.remove_file(f"{export_file}.pdf")
      utils.remove_file(detail_output_file)

  def execute(self, main_model, written_context, generated_context):
    agents = ProductSecurityAgent(main_model, main_model)
    tasks = ProductSecurityTask()

    requirement_refinement_task = tasks.requirement_refinement_task(
      written_requirement=written_context,
      generated_context=generated_context,
      agent=agents.controls_agent()
    )
    output = requirement_refinement_task.execute_sync()
    utils.append_to_file(detail_output_file, output.raw)
    utils.append_to_file(temp_file, output.raw)

    return output.raw
