from textwrap import dedent

from crewai import Agent
from crewai_tools import VisionTool

vision_tool = VisionTool()

class ProductSecurityAgent:
    def __init__(self, main_model, vision_model) -> None:
       self.llm = main_model
       self.vision_llm = vision_model


    def system_information_agent(self):
        return Agent(
            role='Software Architect',
            backstory=dedent(""" You are an expert in software architecture
                        with expertise in understanding the details of a software 
                        by looking at the system software architectural diagram.
                        """),
            goal=dedent("""Properly Analyze the software architectural diagram,
                        break it down into its components, connections between 
                        components and communication protocols. This information 
                        will be used as input into a threat modeling task.
                        """),
            verbose=True,
            allow_delegation=True,
            tools=[vision_tool],
            llm = self.vision_llm
    )
    
    def architectural_analysis_agent(self):
        return Agent(
            role='Security  Architect',
            backstory=dedent(""" You are an experienced security architect. 
                        with expertise in studying software system description 
                        or software architectural diagram to be able breakdown 
                        its components, extract information that would be useful 
                        for threat modeling.
                        """),
            goal=dedent("""Analyze software system description or software 
                        architectural diagram, breakdown its components, extract 
                        information that would be useful for threat modeling.
                        This includes examining the overall system architecture, 
                        identifying security controls, and 
                        assessing data flow to extract information that would 
                        be useful for threat modeling
                """),
            verbose=True,
            allow_delegation=True,
            llm = self.llm
        )
    
    def trust_zone_identification_agent(self):
        return Agent(
            role='Security  Architect',
            backstory=dedent(""" You are an experienced security architect. 
                        with expertise in studying software system description 
                        or software architectural diagram to be able identify
                        trust boundaries or zone that would be useful for 
                        threat modeling.
                        """),
            goal=dedent(""" Analyze software system description or software 
                        architectural diagram, identify trust zone or boundaries
                        that would be useful for threat modeling.
                        """),
            verbose=True,
            allow_delegation=True,
            llm = self.llm
        )

    def threat_scenario_agent(self):
        return Agent(
            role='Senior Security Threat Modeler',
            backstory=dedent(""" You are an experienced Senior Security Threat Modeler. 
                        with expertise in studying software system description 
                        or software architectural diagram to be able to identify threat 
                        scenarios that would be useful for threat modeling.
                        """),
            goal=dedent(""" Properly study the detailed information provided. It contains
                        the system information and trust zone. Use this information to
                        identify realistic threat scenario against the system that would be
                        that would be useful for threat modeling. Ensure that the potential
                        vulnerabilities in each components and its interactions  is considered
                        when creating the threat scenarios.
                        """),
            verbose=True,
            allow_delegation=True,
            llm = self.llm
        )

    def controls_agent(self):
        return Agent(
            role='Senior Security Architect',
            backstory=dedent(""" You are an experienced Senior Security
                        with expertise in studying software system description, security objectives
                        and threat scenario for each component to be able to identify countermeasure
                         that will be the output of a threat modeling task.
                        """),
            goal=dedent(""" Properly study the detailed information provided. It contains
                        the system information and threat scenarios. Use that infromation to 
                        generate well defined countermeansures for threat scenario.
                        """),
            verbose=True,
            allow_delegation=True,
            llm = self.llm
    )

    def requirement_agent(self):
        return Agent(
            role='Senior Security Architect',
            backstory=dedent(""" 
                        Act as a cyber security expert with more than 20 years of experience in 
                        threat modeling. You apply your expertise to studying software system description, 
                        security objectives and threat scenario for each component to be able to generate 
                        security requirement that needs to be meet by the application to mitigate 
                        each threat scenario.
                        """),
            goal=dedent(""" Properly study the detailed information provided. It contains
                        the system information and threat scenarios. Use that information to 
                        generate well defined security requirement that follow a set of presentation
                        format and rule.
                        """),
            verbose=True,
            max_iter = 4,
            allow_delegation=False,
            llm = self.llm
        )
        
    