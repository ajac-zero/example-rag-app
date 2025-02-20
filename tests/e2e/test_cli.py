from typer.testing import CliRunner

from rag.entrypoints.cli import app

runner = CliRunner()

# TODO: The CLI tests could definitely be improved, but I need to do more research on how to test interactive python TUI apps.
def test_chat():
    result = runner.invoke(app)

    assert result.exit_code == 1
