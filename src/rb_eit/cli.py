import click
import numpy as np
import json
from pathlib import Path
from .double_lambda import DoubleLambdaSystem
from .visualization import (
    plot_eit_spectrum,
    plot_comparison,
    plot_transmission_spectrum,
    plot_linewidth_vs_pump_power,
    plot_energy_level_diagram,
    plot_simple_level_diagram,
    plot_detuning_rabi_heatmap,
    plot_3d_surface,
    plot_two_photon_resonance,
    create_interactive_eit_spectrum,
    create_interactive_heatmap,
    create_interactive_3d_surface,
    create_parameter_sweep_comparison
)


def load_config(config_file):
    if config_file:
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}


def create_system_from_config(config):
    return DoubleLambdaSystem(
        isotope=config.get('isotope', 'Rb87'),
        ground_state_1_label=config.get('ground_state_1_label'),
        ground_state_2_label=config.get('ground_state_2_label'),
        excited_state_label=config.get('excited_state_label'),
        pump_rabi_frequency=config.get('pump_rabi_frequency', 2 * np.pi * 10e6),
        probe_rabi_frequency=config.get('probe_rabi_frequency', 2 * np.pi * 1e6),
        pump_detuning=config.get('pump_detuning', 0.0),
        probe_detuning=config.get('probe_detuning', 0.0)
    )


@click.group()
def cli():
    """Rb EIT Simulation and Visualization Tool"""
    pass


@cli.command()
@click.option('--config', type=click.Path(exists=True), help='JSON configuration file')
@click.option('--isotope', default='Rb87', help='Isotope: Rb87 or Rb85')
@click.option('--pump-rabi', type=float, default=10.0, help='Pump Rabi frequency (MHz)')
@click.option('--probe-rabi', type=float, default=1.0, help='Probe Rabi frequency (MHz)')
@click.option('--pump-detuning', type=float, default=0.0, help='Pump detuning (MHz)')
@click.option('--probe-detuning', type=float, default=0.0, help='Probe detuning (MHz)')
@click.option('--detuning-min', type=float, default=-30.0, help='Min detuning for scan (MHz)')
@click.option('--detuning-max', type=float, default=30.0, help='Max detuning for scan (MHz)')
@click.option('--output', '-o', default='eit_spectrum.png', help='Output file path')
@click.option('--no-show', is_flag=True, help='Do not display plot')
def spectrum(config, isotope, pump_rabi, probe_rabi, pump_detuning, probe_detuning,
             detuning_min, detuning_max, output, no_show):
    """Generate EIT spectrum plot"""
    
    if config:
        cfg = load_config(config)
        system = create_system_from_config(cfg)
    else:
        system = DoubleLambdaSystem(
            isotope=isotope,
            pump_rabi_frequency=pump_rabi * 2 * np.pi * 1e6,
            probe_rabi_frequency=probe_rabi * 2 * np.pi * 1e6,
            pump_detuning=pump_detuning * 2 * np.pi * 1e6,
            probe_detuning=probe_detuning * 2 * np.pi * 1e6
        )
    
    plot_eit_spectrum(
        system,
        detuning_range=(detuning_min, detuning_max),
        output_file=output,
        show=not no_show
    )
    click.echo(f"Generated spectrum plot: {output}")


@cli.command()
@click.option('--config', type=click.Path(exists=True), help='JSON configuration file')
@click.option('--isotope', default='Rb87', help='Isotope: Rb87 or Rb85')
@click.option('--pump-rabi', type=float, default=10.0, help='Pump Rabi frequency (MHz)')
@click.option('--probe-rabi', type=float, default=1.0, help='Probe Rabi frequency (MHz)')
@click.option('--output', '-o', default='energy_diagram.png', help='Output file path')
@click.option('--simple', is_flag=True, help='Use simple diagram style')
@click.option('--no-show', is_flag=True, help='Do not display plot')
def energy_diagram(config, isotope, pump_rabi, probe_rabi, output, simple, no_show):
    """Generate energy level diagram"""
    
    if config:
        cfg = load_config(config)
        system = create_system_from_config(cfg)
    else:
        system = DoubleLambdaSystem(
            isotope=isotope,
            pump_rabi_frequency=pump_rabi * 2 * np.pi * 1e6,
            probe_rabi_frequency=probe_rabi * 2 * np.pi * 1e6
        )
    
    if simple:
        plot_simple_level_diagram(system, output_file=output, show=not no_show)
    else:
        plot_energy_level_diagram(system, output_file=output, show=not no_show)
    
    click.echo(f"Generated energy diagram: {output}")


@cli.command()
@click.option('--config', type=click.Path(exists=True), help='JSON configuration file')
@click.option('--isotope', default='Rb87', help='Isotope: Rb87 or Rb85')
@click.option('--pump-rabi', type=float, default=10.0, help='Pump Rabi frequency (MHz)')
@click.option('--probe-rabi', type=float, default=1.0, help='Probe Rabi frequency (MHz)')
@click.option('--detuning-min', type=float, default=-30.0, help='Min detuning for scan (MHz)')
@click.option('--detuning-max', type=float, default=30.0, help='Max detuning for scan (MHz)')
@click.option('--pump-min', type=float, default=1.0, help='Min pump Rabi frequency (MHz)')
@click.option('--pump-max', type=float, default=50.0, help='Max pump Rabi frequency (MHz)')
@click.option('--output', '-o', default='parameter_heatmap.png', help='Output file path')
@click.option('--no-show', is_flag=True, help='Do not display plot')
def heatmap(config, isotope, pump_rabi, probe_rabi, detuning_min, detuning_max,
            pump_min, pump_max, output, no_show):
    """Generate parameter space heatmap"""
    
    if config:
        cfg = load_config(config)
        system = create_system_from_config(cfg)
    else:
        system = DoubleLambdaSystem(
            isotope=isotope,
            pump_rabi_frequency=pump_rabi * 2 * np.pi * 1e6,
            probe_rabi_frequency=probe_rabi * 2 * np.pi * 1e6
        )
    
    plot_detuning_rabi_heatmap(
        system,
        probe_detuning_range=(detuning_min, detuning_max),
        pump_rabi_range=(pump_min, pump_max),
        output_file=output,
        show=not no_show
    )
    click.echo(f"Generated heatmap: {output}")


@cli.command()
@click.option('--config', type=click.Path(exists=True), help='JSON configuration file')
@click.option('--isotope', default='Rb87', help='Isotope: Rb87 or Rb85')
@click.option('--pump-rabi', type=float, default=10.0, help='Pump Rabi frequency (MHz)')
@click.option('--probe-rabi', type=float, default=1.0, help='Probe Rabi frequency (MHz)')
@click.option('--detuning-min', type=float, default=-30.0, help='Min detuning for scan (MHz)')
@click.option('--detuning-max', type=float, default=30.0, help='Max detuning for scan (MHz)')
@click.option('--pump-min', type=float, default=1.0, help='Min pump Rabi frequency (MHz)')
@click.option('--pump-max', type=float, default=50.0, help='Max pump Rabi frequency (MHz)')
@click.option('--output', '-o', default='surface_3d.png', help='Output file path')
@click.option('--no-show', is_flag=True, help='Do not display plot')
def surface(config, isotope, pump_rabi, probe_rabi, detuning_min, detuning_max,
            pump_min, pump_max, output, no_show):
    """Generate 3D surface plot"""
    
    if config:
        cfg = load_config(config)
        system = create_system_from_config(cfg)
    else:
        system = DoubleLambdaSystem(
            isotope=isotope,
            pump_rabi_frequency=pump_rabi * 2 * np.pi * 1e6,
            probe_rabi_frequency=probe_rabi * 2 * np.pi * 1e6
        )
    
    plot_3d_surface(
        system,
        probe_detuning_range=(detuning_min, detuning_max),
        pump_rabi_range=(pump_min, pump_max),
        output_file=output,
        show=not no_show
    )
    click.echo(f"Generated 3D surface: {output}")


@cli.command()
@click.option('--config', type=click.Path(exists=True), help='JSON configuration file')
@click.option('--isotope', default='Rb87', help='Isotope: Rb87 or Rb85')
@click.option('--pump-rabi', type=float, default=10.0, help='Pump Rabi frequency (MHz)')
@click.option('--probe-rabi', type=float, default=1.0, help='Probe Rabi frequency (MHz)')
@click.option('--pump-min', type=float, default=1.0, help='Min pump Rabi frequency (MHz)')
@click.option('--pump-max', type=float, default=50.0, help='Max pump Rabi frequency (MHz)')
@click.option('--probe-min', type=float, default=0.1, help='Min probe Rabi frequency (MHz)')
@click.option('--probe-max', type=float, default=10.0, help='Max probe Rabi frequency (MHz)')
@click.option('--output', '-o', default='interactive_spectrum.html', help='Output HTML file')
def interactive(config, isotope, pump_rabi, probe_rabi, pump_min, pump_max,
                probe_min, probe_max, output):
    """Generate interactive Plotly visualization"""
    
    if config:
        cfg = load_config(config)
        system = create_system_from_config(cfg)
    else:
        system = DoubleLambdaSystem(
            isotope=isotope,
            pump_rabi_frequency=pump_rabi * 2 * np.pi * 1e6,
            probe_rabi_frequency=probe_rabi * 2 * np.pi * 1e6
        )
    
    create_interactive_eit_spectrum(
        system,
        pump_rabi_range=(pump_min, pump_max),
        probe_rabi_range=(probe_min, probe_max),
        output_file=output
    )
    click.echo(f"Generated interactive plot: {output}")


@cli.command()
@click.option('--config', type=click.Path(exists=True), help='JSON configuration file')
@click.option('--isotope', default='Rb87', help='Isotope: Rb87 or Rb85')
@click.option('--probe-rabi', type=float, default=1.0, help='Probe Rabi frequency (MHz)')
@click.option('--detuning-min', type=float, default=-30.0, help='Min detuning for scan (MHz)')
@click.option('--detuning-max', type=float, default=30.0, help='Max detuning for scan (MHz)')
@click.option('--pump-min', type=float, default=1.0, help='Min pump Rabi frequency (MHz)')
@click.option('--pump-max', type=float, default=50.0, help='Max pump Rabi frequency (MHz)')
@click.option('--output', '-o', default='interactive_heatmap.html', help='Output HTML file')
def interactive_heatmap(config, isotope, probe_rabi, detuning_min, detuning_max,
                        pump_min, pump_max, output):
    """Generate interactive Plotly heatmap"""
    
    if config:
        cfg = load_config(config)
        system = create_system_from_config(cfg)
    else:
        system = DoubleLambdaSystem(
            isotope=isotope,
            probe_rabi_frequency=probe_rabi * 2 * np.pi * 1e6
        )
    
    create_interactive_heatmap(
        system,
        probe_detuning_range=(detuning_min, detuning_max),
        pump_rabi_range=(pump_min, pump_max),
        output_file=output
    )
    click.echo(f"Generated interactive heatmap: {output}")


@cli.command()
@click.option('--config', type=click.Path(exists=True), help='JSON configuration file')
@click.option('--isotope', default='Rb87', help='Isotope: Rb87 or Rb85')
@click.option('--probe-rabi', type=float, default=1.0, help='Probe Rabi frequency (MHz)')
@click.option('--detuning-min', type=float, default=-30.0, help='Min detuning for scan (MHz)')
@click.option('--detuning-max', type=float, default=30.0, help='Max detuning for scan (MHz)')
@click.option('--pump-min', type=float, default=1.0, help='Min pump Rabi frequency (MHz)')
@click.option('--pump-max', type=float, default=50.0, help='Max pump Rabi frequency (MHz)')
@click.option('--output', '-o', default='interactive_surface.html', help='Output HTML file')
def interactive_surface(config, isotope, probe_rabi, detuning_min, detuning_max,
                        pump_min, pump_max, output):
    """Generate interactive Plotly 3D surface"""
    
    if config:
        cfg = load_config(config)
        system = create_system_from_config(cfg)
    else:
        system = DoubleLambdaSystem(
            isotope=isotope,
            probe_rabi_frequency=probe_rabi * 2 * np.pi * 1e6
        )
    
    create_interactive_3d_surface(
        system,
        probe_detuning_range=(detuning_min, detuning_max),
        pump_rabi_range=(pump_min, pump_max),
        output_file=output
    )
    click.echo(f"Generated interactive 3D surface: {output}")


if __name__ == '__main__':
    cli()
