import click

from src.pit.cli.add import add


def test_add_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello")
    runner = click.testing.CliRunner()
    result = runner.invoke(add, [str(test_file)])
    assert "Added:" in result.output
