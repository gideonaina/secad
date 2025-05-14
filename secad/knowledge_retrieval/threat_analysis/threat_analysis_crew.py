from dotenv import load_dotenv

from knowledge_retrieval import utils
from knowledge_retrieval.models import ThreatAnalysisContext
from knowledge_retrieval.threat_analysis.threat_analysis_agents import (
  ThreatAnalysisAgent,
)
from knowledge_retrieval.threat_analysis.threat_analysis_tasks import (
  ThreatAnalysisTasks,
)

from rag_management.query_embedding import similarity_search

load_dotenv()

temp_file = "/tmp/threat_model_crew_temp.md"
export_file = "/tmp/threat_model_crew_exported"
detail_output_file = "/tmp/crew_detail.md"

'''
=======================================================
 This is a demostrative of non-agentic execution workflow.
 Notice how state is passed around and how the tasks are executed.
 The tasks are executed in a sequential manner and the output of one task is passed to the next task.
 The tasks are executed in a synchronous manner.
=======================================================
'''

class ThreatAnalysisCrew:
  def __init__(self):
      utils.remove_file(temp_file)
      utils.remove_file(f"{export_file}.docx")
      utils.remove_file(f"{export_file}.pdf")
      utils.remove_file(detail_output_file)

  def execute(self, main_model, context_info: ThreatAnalysisContext):
    agents = ThreatAnalysisAgent(main_model)
    tasks = ThreatAnalysisTasks()

    trust_zone_identification_task = tasks.trust_boundary_identification_task(
      context_info = context_info,
      agent=agents.trust_zone_identification_agent()
    )

    output = trust_zone_identification_task.execute_sync()
    # utils.append_to_file(detail_output_file, output.raw)
    context_info.trust_zone_analysis = output.raw

    threat_scenario_task = tasks.threat_scenario_creation_task(
      context_info = context_info,
      agent=agents.threat_scenario_agent()
    )

    output = threat_scenario_task.execute_sync()

    # utils.append_to_file(detail_output_file, output.raw)

    rag_context = similarity_search(output.raw, collection_name="controls")
    context_info.threat_scenario = output.raw
    context_info.rag_context = rag_context


    control_measure_task = tasks.control_measure_task(
      context_info = context_info,
      agent=agents.controls_agent()
    )
    output = control_measure_task.execute_sync()
    # utils.append_to_file(detail_output_file, output.raw)
    # utils.append_to_file(temp_file, output.raw)

    return output.raw
