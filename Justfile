set dotenv-load

cli:
  @uv run rag-cli

api:
  @uv run rag-api

test:
  @uv run pytest --cov=src/ --cov-report term-missing

tidy:
  @echo "Linting..."
  @uv run ruff check --fix

  @echo "\nFormatting..."
  @uv run ruff format

type-check:
  @uv run mypy src/

graph:
  @uv run pydeps src/rag/

ci:
  just tidy
  just type-check
  just test
