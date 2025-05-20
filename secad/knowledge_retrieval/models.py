
from enum import Enum
from pydantic import BaseModel
from typing import Optional


class DiagramType(str, Enum):
    MMD = "MERMAID"
    IMG = "IMAGE"
    
class ThreatAnalysisContext(BaseModel):
    """
    Context for threat analysis.
    """
    model_config = {
        "frozen": False  # allow modification
    }
    system_information: str
    mermaid_diagram: str
    architectural_diagram_type: Optional[DiagramType] = None
    trust_zone_analysis: Optional[str] = None
    threat_scenario: Optional[str] = None
    controls: Optional[str] = None
    rag_context: Optional[str] = None


    

    
    
    
