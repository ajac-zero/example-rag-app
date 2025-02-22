set dotenv-load

run entrypoint *ARGS:
  @docker compose run --rm rag {{entrypoint}} {{ARGS}}

test tests="":
  @uv run pytest tests/{{tests}} --cov=src/ --cov-report term-missing

tidy:
  @echo "Linting..."
  @uv run ruff check --fix

  @echo "\nFormatting..."
  @uv run ruff format

type-check:
  @echo "Type checking..."
  @uv run mypy src/

graph:
  @echo "Creating dependency graph..."
  @uv run pydeps src/rag/ -o dependency-graph.svg

ci:
  just tidy
  @echo
  just type-check
  @echo
  just test

scaffold:
  @echo "Scaffolding infrastructure..."
  @docker compose --profile infra up -d

teardown:
  @echo "Tearing down infrastructure..."
  @docker compose --profile infra down

create-collection:
  @uvx marimo edit --sandbox infra/qdrant/create_collection.py
