# Define variables for Docker-related tasks
SERVICE_NAME = api
IMAGE_NAME = content-curation-api
DOCKER_COMPOSE_FILE = docker-compose.yml

# Build the Docker image
build:
	docker compose -f $(DOCKER_COMPOSE_FILE) build

# Rebuild the Docker image and start the containers
rebuild:
	docker compose -f $(DOCKER_COMPOSE_FILE) down --rmi all
	docker compose -f $(DOCKER_COMPOSE_FILE) build
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

# Run the Docker container
start:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

# Restart Docker container
restart:
	docker compose -f $(DOCKER_COMPOSE_FILE) down
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

# Stop and remove containers, networks, images, and volumes
stop:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

# Create migration
migrate:
	docker compose exec -it $(SERVICE_NAME) /scripts/migrate-db.sh "$(m)"

# Remove the Docker image
clean:
	docker rmi $(IMAGE_NAME)

# Display logs of the FastAPI service
logs:
	docker compose -f $(DOCKER_COMPOSE_FILE) logs --since=1h $(SERVICE_NAME)

# Run a shell inside the FastAPI container for debugging
shell:
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm $(SERVICE_NAME) sh

# Seed
seed:
	docker compose exec -it $(SERVICE_NAME) /scripts/seeder.sh


# For Formatting and linting tasks
ruff-check:
	ruff check .

ruff-check-fix:
	ruff check . --fix

ruff-check-import-fix:
	ruff check . --select I --fix

ruff-format:
	ruff format .
