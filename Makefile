.PHONY: help install setup run test clean docker-build docker-run docker-stop deploy

help: ## Show this help message
	@echo "PDF Knowledge Graph Generator - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt
	python -m spacy download en_core_web_sm

setup: ## Run complete setup (virtual env + dependencies)
	@chmod +x scripts/setup.sh
	./scripts/setup.sh

run: ## Run the application locally
	@chmod +x scripts/run.sh
	./scripts/run.sh

test: ## Run tests
	pytest tests/ -v

clean: ## Clean up temporary files and caches
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

docker-build: ## Build Docker image
	docker build -t pdf-knowledge-graph .

docker-run: ## Run with Docker Compose
	docker-compose up --build -d

docker-stop: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

deploy: ## Deploy to production (placeholder)
	@echo "Deployment not configured. Please configure your deployment pipeline."

lint: ## Run code linting
	flake8 app.py
	black --check app.py
	isort --check-only app.py

format: ## Format code
	black app.py
	isort app.py

requirements: ## Update requirements.txt
	pip freeze > requirements.txt

venv: ## Create virtual environment
	python3 -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"

dev: ## Run in development mode
	STREAMLIT_SERVER_HEADLESS=false streamlit run app.py --server.port=8501

prod: ## Run in production mode
	STREAMLIT_SERVER_HEADLESS=true streamlit run app.py --server.port=8501 --server.address=0.0.0.0
