"""
Command-line interface for the FWM simulator.
"""

import click

from fwm_sim import __version__


@click.group()
@click.version_option(version=__version__)
def main():
    """
    FWM Simulator - Rb double-lambda Four-Wave Mixing simulator.

    Use the subcommands to simulate, plot, and export FWM data.
    """
    pass


@main.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to simulation configuration file",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="output",
    help="Output directory for simulation results",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def simulate(config, output, verbose):
    """
    Run a Four-Wave Mixing simulation.

    This command will execute the FWM simulation based on the provided
    configuration and save the results to the specified output directory.
    """
    click.echo("FWM Simulate command - Not yet implemented")
    if config:
        click.echo(f"Config file: {config}")
    click.echo(f"Output directory: {output}")
    if verbose:
        click.echo("Verbose mode enabled")


@main.command()
@click.option(
    "--input",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="Path to simulation results file",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output path for plot (if not specified, displays interactively)",
)
@click.option(
    "--plot-type",
    "-t",
    type=click.Choice(["interactive", "static"], case_sensitive=False),
    default="interactive",
    help="Type of plot to generate",
)
def plot(input, output, plot_type):
    """
    Plot FWM simulation results.

    Visualize the results from a previous simulation run using matplotlib
    or plotly for interactive visualization.
    """
    click.echo("FWM Plot command - Not yet implemented")
    click.echo(f"Input file: {input}")
    if output:
        click.echo(f"Output file: {output}")
    click.echo(f"Plot type: {plot_type}")


@main.command()
@click.option(
    "--input",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="Path to simulation results file",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    required=True,
    help="Output path for exported data",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["csv", "json", "hdf5"], case_sensitive=False),
    default="csv",
    help="Export format",
)
def export(input, output, format):
    """
    Export FWM simulation results to various formats.

    Convert simulation results to different file formats for further
    analysis or sharing.
    """
    click.echo("FWM Export command - Not yet implemented")
    click.echo(f"Input file: {input}")
    click.echo(f"Output file: {output}")
    click.echo(f"Export format: {format}")


if __name__ == "__main__":
    main()
