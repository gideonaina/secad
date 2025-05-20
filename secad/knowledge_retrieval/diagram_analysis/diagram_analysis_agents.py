from textwrap import dedent

from crewai import Agent
from crewai_tools import VisionTool

vision_tool = VisionTool()


class DiagramAnalysisAgents:

    def system_information_agent(self, vision_llm):
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
            allow_delegation=False,
            tools=[VisionTool()],
            llm = vision_llm
    )
    

    def system_information_as_mermaid_agent(self, vision_llm):
        return Agent(
            role='Software Architect',
            backstory=dedent(""" You are an expert in software architecture
                        with expertise in understanding the details of a software 
                        by looking at the system software architectural diagram.
                        """),
            goal=dedent("""Properly Analyze the software architectural diagram,
                        and redraw it in mermaid format. The mermaid diagram should be
                        a proper representation of the system architecture.
                        """),
            verbose=True,
            allow_delegation=False,
            tools=[VisionTool()],
            llm = vision_llm
    )

    def mermaid_validation_agent(self, llm):
        return Agent(
            role='Software Engineer',
            backstory=dedent(""" You are a software engineer  with expertise in
                        creating software architectural diagram in mermaid format.
                        You are also an expert in validating the correctness of
                        mermaid diagrams.
                        """),
            goal=dedent("""Properly Analyze a mermaid architectural diagram, 
                        if it has any errors correct then.
                        """),
            verbose=True,
            allow_delegation=False,
            llm = llm
    )



    

