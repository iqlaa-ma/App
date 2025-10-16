.PHONY: help build up down restart logs shell test clean generate-key setup install run dev stop ps health

# Default target
.DEFAULT_GOAL := help

# Variables
DOCKER_COMPOSE = docker-compose
DOCKER = docker
CONTAINER_NAME = fastapi-auth-api
IMAGE_NAME = fastapi-auth-backend
PYTHON = python3

# Colors for terminal output
GREEN = \033[0;32m
YELLOW = \033[0;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)FastAPI Authentication Backend - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ============================================================================
# Docker Commands
# ============================================================================

build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	$(DOCKER_COMPOSE) build
	@echo "$(GREEN)✓ Build complete!$(NC)"

up: ## Start all containers
	@echo "$(GREEN)Starting containers...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✓ Containers started!$(NC)"
	@echo "$(YELLOW)API available at: http://localhost:8000$(NC)"
	@echo "$(YELLOW)Documentation at: http://localhost:8000/docs$(NC)"

down: ## Stop and remove all containers
	@echo "$(YELLOW)Stopping containers...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✓ Containers stopped!$(NC)"

restart: down up ## Restart all containers

logs: ## Show container logs (use CTRL+C to exit)
	$(DOCKER_COMPOSE) logs -f api

logs-tail: ## Show last 100 lines of logs
	$(DOCKER_COMPOSE) logs --tail=100 api

shell: ## Open shell in running container
	@echo "$(GREEN)Opening shell in container...$(NC)"
	$(DOCKER) exec -it $(CONTAINER_NAME) /bin/bash

ps: ## Show running containers
	$(DOCKER_COMPOSE) ps

stop: ## Stop containers without removing them
	$(DOCKER_COMPOSE) stop

# ============================================================================
# Testing Commands
# ============================================================================

test: ## Run tests inside Docker container
	@echo "$(GREEN)Running tests...$(NC)"
	$(DOCKER) exec $(CONTAINER_NAME) pytest -v
	@echo "$(GREEN)✓ Tests complete!$(NC)"

test-coverage: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	$(DOCKER) exec $(CONTAINER_NAME) pytest --cov=app --cov-report=term-missing tests/
	@echo "$(GREEN)✓ Coverage report complete!$(NC)"

test-local: ## Run tests locally (requires local setup)
	@echo "$(GREEN)Running tests locally...$(NC)"
	pytest -v
	@echo "$(GREEN)✓ Tests complete!$(NC)"

# ============================================================================
# API Testing Commands
# ============================================================================

health: ## Check API health
	@echo "$(GREEN)Checking API health...$(NC)"
	@curl -s http://localhost:8000/health | python3 -m json.tool || echo "$(RED)API not responding$(NC)"

test-register: ## Test user registration
	@echo "$(GREEN)Testing user registration...$(NC)"
	@curl -X POST http://localhost:8000/auth/register \
		-H "Content-Type: application/json" \
		-d '{"email":"test@example.com","username":"testuser","password":"Test1234!"}' \
		| python3 -m json.tool

test-login: ## Test user login
	@echo "$(GREEN)Testing user login...$(NC)"
	@curl -X POST http://localhost:8000/auth/login \
		-H "Content-Type: application/json" \
		-d '{"email":"test@example.com","password":"Test1234!"}' \
		| python3 -m json.tool

test-me: ## Test protected endpoint (set TOKEN variable first)
	@echo "$(GREEN)Testing protected endpoint...$(NC)"
	@if [ -z "$(TOKEN)" ]; then \
		echo "$(RED)Error: TOKEN variable not set$(NC)"; \
		echo "$(YELLOW)Usage: make test-me TOKEN=your_jwt_token$(NC)"; \
		exit 1; \
	fi
	@curl -X GET http://localhost:8000/users/me \
		-H "Authorization: Bearer $(TOKEN)" \
		| python3 -m json.tool

test-all-endpoints: ## Test all endpoints in sequence
	@echo "$(GREEN)Testing all endpoints...$(NC)"
	@echo "\n$(YELLOW)1. Health Check:$(NC)"
	@make health
	@echo "\n$(YELLOW)2. User Registration:$(NC)"
	@make test-register
	@echo "\n$(YELLOW)3. User Login:$(NC)"
	@make test-login
	@echo "\n$(GREEN)✓ All endpoint tests complete!$(NC)"

# ============================================================================
# Setup Commands
# ============================================================================

generate-key: ## Generate a new SECRET_KEY
	@echo "$(GREEN)Generated SECRET_KEY:$(NC)"
	@$(PYTHON) -c "import secrets; print(secrets.token_hex(32))"
	@echo ""
	@echo "$(YELLOW)Copy this key to your .env file$(NC)"

setup: ## Initial setup - creates .env if missing
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)Creating .env file...$(NC)"; \
		echo "DATABASE_URL=sqlite:///./data/app.db" > .env; \
		echo "SECRET_KEY=$$(python3 -c 'import secrets; print(secrets.token_hex(32))')" >> .env; \
		echo "ALGORITHM=HS256" >> .env; \
		echo "ACCESS_TOKEN_EXPIRE_MINUTES=30" >> .env; \
		echo "APP_NAME=Mobile Auth API" >> .env; \
		echo "DEBUG=True" >> .env; \
		echo "$(GREEN)✓ .env file created!$(NC)"; \
	else \
		echo "$(YELLOW).env file already exists$(NC)"; \
	fi
	@mkdir -p data
	@echo "$(GREEN)✓ Setup complete!$(NC)"

install: ## Install dependencies locally (for local development)
	@echo "$(GREEN)Installing dependencies...$(NC)"
	pip install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed!$(NC)"

create-dirs: ## Create necessary directories
	@mkdir -p data tests app/auth app/users
	@touch app/__init__.py app/auth/__init__.py app/users/__init__.py tests/__init__.py
	@echo "$(GREEN)✓ Directories created!$(NC)"

# ============================================================================
# Development Commands
# ============================================================================

dev: setup build up ## Complete development setup (setup + build + run)
	@echo ""
	@echo "$(GREEN)════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Development environment ready!$(NC)"
	@echo "$(GREEN)════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "  $(YELLOW)API:$(NC)          http://localhost:8000"
	@echo "  $(YELLOW)Docs:$(NC)         http://localhost:8000/docs"
	@echo "  $(YELLOW)ReDoc:$(NC)        http://localhost:8000/redoc"
	@echo "  $(YELLOW)Health:$(NC)       http://localhost:8000/health"
	@echo ""
	@echo "$(YELLOW)Useful commands:$(NC)"
	@echo "  make logs          - View logs"
	@echo "  make test          - Run tests"
	@echo "  make test-register - Test registration"
	@echo "  make shell         - Open container shell"
	@echo ""

run: up ## Alias for 'up' - Start containers

rebuild: ## Rebuild and restart containers
	@echo "$(GREEN)Rebuilding containers...$(NC)"
	$(DOCKER_COMPOSE) up -d --build
	@echo "$(GREEN)✓ Rebuild complete!$(NC)"

# ============================================================================
# Cleanup Commands
# ============================================================================

clean: ## Remove containers, images, and volumes
	@echo "$(YELLOW)Cleaning up...$(NC)"
	$(DOCKER_COMPOSE) down -v
	$(DOCKER) rmi $(IMAGE_NAME) 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete!$(NC)"

clean-db: ## Remove database file
	@echo "$(YELLOW)Removing database...$(NC)"
	rm -f data/app.db data/test.db
	@echo "$(GREEN)✓ Database removed!$(NC)"

clean-all: clean clean-db ## Complete cleanup (containers + database)
	@echo "$(GREEN)✓ Complete cleanup done!$(NC)"

prune: ## Remove all unused Docker resources
	@echo "$(YELLOW)Pruning Docker resources...$(NC)"
	$(DOCKER) system prune -af
	@echo "$(GREEN)✓ Prune complete!$(NC)"

# ============================================================================
# Database Commands
# ============================================================================

db-shell: ## Open SQLite shell for database
	@echo "$(GREEN)Opening database shell...$(NC)"
	$(DOCKER) exec -it $(CONTAINER_NAME) sqlite3 /app/data/app.db

db-backup: ## Backup database
	@echo "$(GREEN)Backing up database...$(NC)"
	@mkdir -p backups
	@cp data/app.db backups/app.db.$$(date +%Y%m%d_%H%M%S)
	@echo "$(GREEN)✓ Database backed up!$(NC)"

# ============================================================================
# Quick Start Commands
# ============================================================================

quick-start: ## Quick start guide
	@echo "$(GREEN)════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  FastAPI Auth Backend - Quick Start Guide$(NC)"
	@echo "$(GREEN)════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)Step 1:$(NC) Setup environment"
	@echo "  $$ make setup"
	@echo ""
	@echo "$(YELLOW)Step 2:$(NC) Build and start containers"
	@echo "  $$ make dev"
	@echo ""
	@echo "$(YELLOW)Step 3:$(NC) Test the API"
	@echo "  $$ make test-all-endpoints"
	@echo ""
	@echo "$(YELLOW)Step 4:$(NC) Run tests"
	@echo "  $$ make test"
	@echo ""
	@echo "$(GREEN)That's it! Your API is ready.$(NC)"
	@echo ""

# ============================================================================
# Status and Info Commands
# ============================================================================

status: ## Show status of all services
	@echo "$(GREEN)Service Status:$(NC)"
	@$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "$(GREEN)API Status:$(NC)"
	@make health 2>/dev/null || echo "$(RED)API not responding$(NC)"

info: ## Show system information
	@echo "$(GREEN)System Information:$(NC)"
	@echo "Docker version: $$(docker --version)"
	@echo "Docker Compose version: $$(docker-compose --version)"
	@echo "Python version: $$(python3 --version)"
	@echo ""
	@echo "$(GREEN)Project Information:$(NC)"
	@echo "Container name: $(CONTAINER_NAME)"
	@echo "Image name: $(IMAGE_NAME)"
	@echo ""