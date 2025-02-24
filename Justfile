set dotenv-load

_list:
  @just --list --unsorted

# Run the application stack with (`cli`, `api`) entrypoint with `args`
run entrypoint *args:
  @docker compose run --rm rag {{entrypoint}} {{args}}

# Start compose containers in the background
scaffold:
  @echo "Scaffolding infrastructure..."
  @docker compose up -d

# Remove compose containers from the background
teardown:
  @echo "Tearing down infrastructure..."
  @docker compose down

# Lint and format with **Ruff**
tidy:
  @echo "Linting..."
  @uv run ruff check --fix

  @echo "\nFormatting..."
  @uv run ruff format

# Type check with **Mypy**
type-check:
  @echo "Type checking..."
  @uv run mypy src/

# Run (`e2e`, `integration`, `unit`) tests; If none specified, run all tests
test tests="":
  @echo "Testing..."
  @uv run pytest tests/{{tests}} --cov=src/ --cov-report term-missing

# Run CI checks locally (`tidy` -> `type-check` -> `test`)
ci:
  @just tidy
  @echo
  @just type-check
  @echo
  @just test

# Generate dependency graph with **Pydeps**
graph:
  @echo "Creating dependency graph..."
  @uv run pydeps src/rag/ -o dependency-graph.svg

# Start data ingestion pipeline with **Marimo**
create-collection:
  @uvx marimo edit --sandbox infra/qdrant/create_collection.py

# `build` or `run` the project container with `args`
container cmd *args:
  @just _container-{{cmd}} {{args}}

_container-build *args:
  @docker build -t rag-container:latest {{args}} .

_container-run *args:
  @docker run --rm -it rag-container:latest {{args}}
