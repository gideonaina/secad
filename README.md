# SECAD

## Summary
SECAD is an **agentic, AI-powered** security advisor that can be used to augment security workflows. 
For more details read: 
https://medium.com/@gideonaina/workflow-augmentation-with-multi-agent-ai-system-3c3223c948dc
 


## System Architecture.
The architecture diagram below illustrates the different layers and complexities of the application.

#### 4.1: Level 1 - System Context.
![screenshot](arch/SystemContext_v3-Level_1_Context.png)

This provide a high level view of the system and its components.

#### 4.2: Level 2 - Data Processing Service. Container
![screenshot](arch/SystemContext_v3-Level-2_DPS.png)

The goal of this service is to extract information from all enterprise sources or knowledge bases. As data is placed in an object store, an event is fired that places the data in a queue for processing. The data pre-processor takes the data off the queue and processes it according to the data type (document, picture, audio, or video).


#### 4.3: Level 2 - RAG Management Service Container.
![screenshot](arch/SystemContext_v3-Level-2_RMS.png)

The data from the Data Processing Service is sent here. The data is first chunked according to a pre-determined chunking metric. Embedding is created from this chunk and saved in a vector database (Postgres with PG Vector in the current case).

#### 4.4: Level 2 - Knowledge Retrieval Service Container.
![screenshot](arch/SystemContext_v3-Level-2_KRS.png)

The Knowledge Retrieval Service uses augmented prompts with specialized AI agents to get the best answer for a task assigned.

