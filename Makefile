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
	@awk -F: '/^[a-zA-Z0-9][^:]*:/ {print $$1}' Makefile

full-llm:
	@echo Starts local deployment of LLM with chat Interface
	@echo "Running with LOCAL_LLM=$(LOCAL_LLM)"
	LOCAL_LLM=$(LOCAL_LLM) $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up --build

llm-only:
	@echo Starts on the LLM container
	@echo "Running ONLY services with LOCAL_LLM=$(LOCAL_LLM)"
	LOCAL_LLM=$(LOCAL_LLM) $(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up model_loader --build

rag:
	@echo Launches the RAG service
	@echo "Running RAG"
	$(DOCKER_COMPOSE) -f $(RAG_COMPOSE_FILE) up --build

stop-rag:
	@echo stops the RAG service
	$(DOCKER_COMPOSE) -f $(RAG_COMPOSE_FILE) down

stop-llm:
	@echo stops the LLM service
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down

clean:
	@echo remove the containers setup by the LLM service
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down -v

clean-rag:
	@echo remove the containers setup by the RAG service
	$(DOCKER_COMPOSE) -f $(RAG_COMPOSE_FILE) down -v

tear-rag:
	@echo stops RAG service, removes the container and volumes
	$(DOCKER_COMPOSE) -f $(RAG_COMPOSE_FILE) down -v && \
	docker stop $(docker ps -aq) && \
	docker volume rm $(docker volume ls -q)
nuke:
	@echo remove all containers and volumes on the host machine
	docker stop $$(docker ps -aq) && \
	docker volume rm $$(docker volume ls -q)

notebook:
	@echo start a Jupyter notebook
	docker network inspect ragnet >/dev/null 2>&1 || docker network create ragnet
	docker run -it --rm -p 10000:8888 --network ragnet -v "${PWD}":/home/jovyan/work quay.io/jupyter/datascience-notebook:2024-05-27

test:
	@echo test port availability
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
