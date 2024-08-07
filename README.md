# Knowledge Extraction System.

## 1.0: Problem Statement.
LLM are a useful piece of technology for encoding  information, trained on vast datasets to understand and generate human-like text. They excel in extracting and synthesizing knowledge from diverse sources, making them powerful for information retrieval. However, LLMs can struggle with providing precise and relevant information within user prompts due to potential biases, overfitting, and lack of specific context. Privacy concerns arise as LLMs may inadvertently retain and expose sensitive data from their training sets, risking user confidentiality and data security. When organization use 3rd LLM API, there also risk providing propietary to the model that can later be used to train it.
Although a very versatile tool for any domain, these issue limit its rate of adoption at enterprise

## 2.0: Solution.
The goal of this project is to provide a template for adoption of AI (specificially LLM) for various enterprise task such that the identified risks and problems are mitigated to some extent.

## 3.0 Summary.
This repository contains various components of the Knowledge Extraction System (KES). The KES is designed to deliver relevant in-context information based on user prompts or questions. The final result presented to the user consolidates information from multiple sources. By leveraging Retrieval-Augmented Generation (RAG), the system ensures that the information provided is highly relevant, minimizing the risk of hallucinations or the LLM relying solely on its training data.
KES can be adopted for use in any domain of work or life where there is need relevant information having specific context without least chance of hallucination is needed.

## 4.0: System Architecture.
The architecture diagram below illustrates the different layers and complexities of the application. Level 1 presents a high-level overview, while subsequent levels (Level 2) delves into specific components to provide more detailed information.

#### 4.1: Level 1 - System Context.
![screenshot](arch/SystemContext_v2-Level-1_Context.png)

This provide a high level view of the system and its components.

#### 4.2: Level 2 - Data Processing Service. Container
![screenshot](arch/SystemContext_v2-Level-2_DPS.png)

The goal of this service is to extract information from all enterprise sources or knowledge base.
As data is place in an object store, an event is fired that places the data in a queue for processing.
The data pre-processor takes the data off the queue and processes it according to the data type (document, picture, audio or video).


#### 4.3: Level 2 - RAG Management Service Container.
![screenshot](arch/SystemContext_v2-Level-2_RMS.png)

The data from the Data Processing Service is sent here. The data is first chunked according to pre-determined chunking metric. Embedding are creaed from this chunk anf safed in a vector database (Postgres with PG Vector in the current case).

#### 4.4: Level 2 - Knowledge Retrieval Service Container.
![screenshot](arch/SystemContext_v2-Level-2_KRS.png)

The Knowledge Retrieval Service uses augumented prompt with specilized AI agent to get the best answer for task assigned.

## 4.0: Implementation

### 4.1: Code Repo

WIP

### 4.2: Use Cases

As previously mentioned, KES can be used in any domain for any task that requires information with a reasonable amount of context and fewer generated ideas. Below are some use cases currently being explored:

**Use Case 1:   Security Architect KES**:

A security architect performs many tasks that contribute to the security of enterprise software systems. Some of those include Security Review, Code Review, and Threat Modeling. To properly perform these tasks, the Security Architect needs detailed context of the application being reviewed in various dimensions. The use of "various dimensions" here means all the information the Security Architect needs to gather to perform their tasks. These include: 
- System Understanding
- System Components
- Data Dictionary
- Trust Boundaries
- Threat Scenarios
- Countermeasures

To use KES to perform the role of a Security Architect, one needs to be able to provide the LLM with the following contextual information:
- Initial prompt: This will be in the form of an architectural diagram or detailed system description
- Enterprise Security Requirements: These are the high-level security requirements defined by the product security team. The generic security requirements serve to guide security reviews in various domains. These will include Data Transfer Security Requirements, Network Security Requirements, Cloud Security Requirements, IAM Security Requirements, etc. Each of these is organization and (sometimes product) specific.
- Governance, Risk, and Compliance (GRC) Policies: These are policies defined by the GRC team to provide governance and compliance guidance.

By providing the contextual information as a RAG and utilizing an AI agent to orchestrate the steps for each task, one can easily scale the work being done by security architects.

**Use Case 2: Security Test KES**:

WIP

**Use Case 3: Real Estate Analysis KES**:

WIP

### 4.2: Reusable Framework

The KES framework is setup in such a way that new use cases can be easily added with minimum setup. The new use case will take advantage of the infrastructure already setup.
