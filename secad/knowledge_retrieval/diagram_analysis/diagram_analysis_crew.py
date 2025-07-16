from knowledge_retrieval.diagram_analysis.diagram_analysis_agents import (
DiagramAnalysisAgents,
) 
from knowledge_retrieval.diagram_analysis.diagram_analysis_tasks import (
    DiagramAnalysisTasks,
)
from knowledge_retrieval.models import ThreatAnalysisContext, DiagramType

class DiagramAnalysisCrew:
    def __init__(self):
        self.agents = DiagramAnalysisAgents()
        self.tasks = DiagramAnalysisTasks()


    def run_mermaid(self, vision_llm, mermaid_diagram) -> ThreatAnalysisContext:
        mermaid_diagram_agent = self.agents.system_information_as_mermaid_agent(vision_llm)
        mermaid_diagram_task = self.tasks.mermaid_architecture_diagram_analysis_task(mermaid_diagram, mermaid_diagram_agent)
        
        system_info = mermaid_diagram_task.execute_sync()

        return ThreatAnalysisContext(
            system_information=system_info.raw,
            mermaid_diagram=mermaid_diagram,
            architectural_diagram_type= DiagramType.MMD
        )
    
    def run_image(self, vision_llm, image_path) -> ThreatAnalysisContext:
        image_agent = self.agents.system_information_agent(vision_llm)
        mermaid_diagram_task = self.tasks.image_architecture_diagram_analysis_task(image_path, image_agent)

        system_info = mermaid_diagram_task.execute_sync()

        mermaid_diagram_agent = self.agents.system_information_as_mermaid_agent(vision_llm)
        mermaid_diagram_task = self.tasks.architecture_image_analysis_as_mermaid_task(image_path, mermaid_diagram_agent)
        mmd_diagram = mermaid_diagram_task.execute_sync()

        validation_agent = self.agents.mermaid_validation_agent(vision_llm)
        validation_task = self.tasks.mermaid_diagram_validation_task(mermaid_graph=mmd_diagram.raw, agent=validation_agent)
        validated_mmd_diagram = validation_task.execute_sync()


        return ThreatAnalysisContext(
            system_information=system_info.raw,
            mermaid_diagram=validated_mmd_diagram.raw,
            architectural_diagram_type= DiagramType.IMG
        )
    
    def run_mermaid_description(self, llm, mermaid_diagram) -> str:
        mermaid_diagram_agent = self.agents.mermaid_system_information_agent(llm)
        mermaid_diagram_task = self.tasks.mermaid_architecture_diagram_analysis_task(mermaid_diagram, mermaid_diagram_agent)

        system_info = mermaid_diagram_task.execute_sync()   

        return system_info.raw