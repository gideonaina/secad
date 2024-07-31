# Makefile for Docker Compose operations

# Define Docker Compose file
COMPOSE_FILE := llm.docker-compose.yml
RAG_COMPOSE_FILE := rag.docker-compose.yml
DOCKER_COMPOSE := docker compose

LOCAL_LLM ?= llama3

.PHONY: help start stop clean

# ANSI color codes
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help:
	@echo "Usage:"
	@echo "  make start    - Start Docker Compose"
	@echo "  make stop     - Stop Docker Compose"
	@echo "  make clean    - Stop Docker Compose and remove volumes"

start:
	@echo "Running with LOCAL_LLM=$(LOCAL_LLM)"
	LOCAL_LLM=$(LOCAL_LLM) $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up --build

llm: 
	@echo "Running ONLY services with LOCAL_LLM=$(LOCAL_LLM)"
	LOCAL_LLM=$(LOCAL_LLM) $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up model_loader --build

rag:
	@echo "Running RAG"
	$(DOCKER_COMPOSE) -f $(RAG_COMPOSE_FILE) up --build

stop-rag:
	$(DOCKER_COMPOSE) -f $(RAG_COMPOSE_FILE) down

stop:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down

clean:
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down -v

clean-rag:
	$(DOCKER_COMPOSE) -f $(RAG_COMPOSE_FILE) down -v

tear-rag:
	$(DOCKER_COMPOSE) -f $(RAG_COMPOSE_FILE) down -v && \
	docker stop $(docker ps -aq) && \
	docker volume rm $(docker volume ls -q)
nuke:
	docker volume rm $(docker volume ls -q)

notebook:
	docker network inspect ragnet >/dev/null 2>&1 || docker network create ragnet
	docker run -it --rm -p 10000:8888 --network ragnet -v "${PWD}":/home/jovyan/work quay.io/jupyter/datascience-notebook:2024-05-27

embed:
	cd src && python data_prep.py -f /Users/gideonaina/dev/local-llm/knowledge_docs/PCI-DSS-v4_0.pdf -c pci-v4-0
	cd src && python data_prep.py -f /Users/gideonaina/dev/local-llm/knowledge_docs/nist.pdf -c container_sec

test:
	@echo "------- Checking Port 11434 -----"
	@timeout 2s curl -sf http://localhost:11434 > /dev/null && echo "$(GREEN)http://localhost:11434 ok$(NC)" || echo "$(RED)http://localhost:11434 error$(NC)"
	@timeout 2s curl -sf http://127.0.0.1:11434 > /dev/null && echo "$(GREEN)http://127.0.0.1:11434 ok$(NC)"|| echo "$(RED)http://127.0.0.1:11434 error$(NC)"
	@timeout 2s curl -sf http://host.docker.internal:11434 > /dev/null && echo "$(GREEN)host.docker.internal:11434 ok$(NC)"|| echo "$(RED)host.docker.internal:11434 error$(NC)"
	@timeout 2s curl -sf http://0.0.0.0:11434 > /dev/null && echo "$(GREEN)0.0.0.0:11434 ok$(NC)"|| echo "$(RED)0.0.0.0:11434 error$(NC)"
	@timeout 2s curl -sf http://ollama:11434 > /dev/null && echo "$(GREEN)ollama:11434 ok$(NC)"|| echo "$(RED)ollama:11434 error$(NC)"
	
	@echo "---- Checking Port 8080 -----"
	@timeout 2s curl -sf http://localhost:8080 > /dev/null && echo "$(GREEN)http://localhost:8080 ok$(NC)"|| echo "$(RED)http://localhost:8080 error$(NC)"
	@timeout 2s curl -sf http://127.0.0.1:8080 > /dev/null && echo "$(GREEN)http://127.0.0.1:8080 ok$(NC)"|| echo "$(RED)http://127.0.0.1:8080 error$(NC)"
	@timeout 2s curl -sf http://host.docker.internal:8080 > /dev/null && echo "$(GREEN)host.docker.internal:8080 ok$(NC)"|| echo "$(RED)host.docker.internal:8080 error$(NC)"
	@timeout 2s curl -sf http://0.0.0.0:8080 > /dev/null && echo "$(GREEN)0.0.0.0:8080 ok$(NC)"|| echo "$(RED)0.0.0.0:8080 error$(NC)"
	@timeout 2s curl -sf http://open-webui:8080 > /dev/null && echo "$(GREEN)open-webui:8080 ok$(NC)"|| echo "$(RED)open-webui:8080 error$(NC)"
	
	@echo "---- Checking Port 3000 -----"
	@timeout 2s curl -sf http://localhost:3000 > /dev/null && echo "$(GREEN)http://localhost:3000 ok$(NC)"|| echo "$(RED)http://localhost:3000 error$(NC)"
	@timeout 2s curl -sf http://127.0.0.1:3000 > /dev/null && echo "$(GREEN)http://127.0.0.1:3000 ok$(NC)"|| echo "$(RED)http://127.0.0.1:3000 error$(NC)"
	@timeout 2s curl -sf http://host.docker.internal:3000 > /dev/null && echo "$(GREEN)host.docker.internal:3000 ok$(NC)"|| echo "$(RED)host.docker.internal:3000 error$(NC)"
	@timeout 2s curl -sf http://0.0.0.0:3000 > /dev/null && echo "$(GREEN)0.0.0.0:3000 ok$(NC)"|| echo "$(RED)0.0.0.0:3000 error$(NC)"
	@timeout 2s curl -sf http://open-webui:3000 > /dev/null && echo "$(GREEN)open-webui:3000 ok$(NC)"|| echo "$(RED)open-webui:3000 error$(NC)"
