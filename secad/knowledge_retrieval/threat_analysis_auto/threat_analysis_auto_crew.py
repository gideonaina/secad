from dotenv import load_dotenv

from crewai import Crew

from knowledge_retrieval import utils
from knowledge_retrieval.models import ThreatAnalysisContext
from knowledge_retrieval.threat_analysis_auto.threat_analysis_auto_agents import (
  ThreatAnalysisAutoAgent,
)
from knowledge_retrieval.threat_analysis_auto.threat_analysis_auto_tasks import (
  ThreatAnalysisAutoTasks,
)

from rag_management.query_embedding import similarity_search

load_dotenv()

'''
=======================================================
 This is demostrates an agentic execution workflow.
 Notice how the agents are suppose to figure out  how to
 get the information for their input.
=======================================================
'''

class ThreatAnalysisAutoCrew:


  def execute(self, main_model, prompt):
    agents = ThreatAnalysisAutoAgent(main_model)
    tasks = ThreatAnalysisAutoTasks()

#   Trust Zone Identification
    trust_zone_analyst = agents.trust_zone_identification_agent()
    trust_zone_identification_task = tasks.trust_boundary_identification_task(
        agent=trust_zone_analyst
      )
    
#   Threat Scenario Generation
    threat_analyst = agents.threat_scenario_agent()
    threat_scenario_task = tasks.threat_scenario_creation_task(
      agent=threat_analyst
    )

#   Control Measure Generation
    controls_researcher = agents.controls_agent()
    control_measure_task = tasks.control_measure_task(
      agent=controls_researcher
    )

    crew = Crew(agents=[trust_zone_analyst, threat_analyst, controls_researcher], 
                tasks=[trust_zone_identification_task, threat_scenario_task, control_measure_task])
    
    try:
      result = crew.kickoff(inputs={"system_information": prompt["system_information"], "mermaid_diagram": prompt["mermaid_diagram"]})
    except Exception as e:
      print(f"Error during threat model execution: {e}")
      print(f"Prompt: {prompt}")
      raise RuntimeError(f"Error generating threat model. Error: {e}")
    

    return result
