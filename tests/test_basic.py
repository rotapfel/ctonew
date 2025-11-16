"""
Basic tests for the FWM simulator package.
"""

import fwm_sim
from click.testing import CliRunner
from fwm_sim.cli import main


def test_version():
    """Test that the package version is defined."""
    assert hasattr(fwm_sim, "__version__")
    assert isinstance(fwm_sim.__version__, str)
    assert len(fwm_sim.__version__) > 0


def test_cli_help():
    """Test that the CLI help command works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "FWM Simulator" in result.output
    assert "simulate" in result.output
    assert "plot" in result.output
    assert "export" in result.output


def test_cli_version():
    """Test that the CLI version command works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert fwm_sim.__version__ in result.output


def test_simulate_command_help():
    """Test that the simulate command help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["simulate", "--help"])
    assert result.exit_code == 0
    assert "simulate" in result.output.lower()
    assert "configuration" in result.output.lower()


def test_plot_command_help():
    """Test that the plot command help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["plot", "--help"])
    assert result.exit_code == 0
    assert "plot" in result.output.lower()
    assert "results" in result.output.lower()


def test_export_command_help():
    """Test that the export command help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["export", "--help"])
    assert result.exit_code == 0
    assert "export" in result.output.lower()
    assert "format" in result.output.lower()


def test_simulate_command_basic():
    """Test that the simulate command runs without errors (placeholder)."""
    runner = CliRunner()
    result = runner.invoke(main, ["simulate"])
    assert result.exit_code == 0
    assert "Not yet implemented" in result.output
