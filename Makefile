SERVICE=app

build:
	@echo "🚀 Building Docker image..."
	docker compose build

up:
	@echo "📦 Starting container..."
	docker compose up -d

down:
	@echo "🧹 Stopping and removing containers..."
	docker compose down

logs:
	@echo "📜 Showing logs..."
	docker compose logs -f $(SERVICE)

shell:
	@echo "🔧 Opening shell inside container..."
	docker compose exec $(SERVICE) sh

clean:
	@echo "🔥 Removing all Docker data..."
	docker compose down -v --rmi all --remove-orphans

rebuild: clean build up
