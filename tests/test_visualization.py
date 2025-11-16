import pytest
import numpy as np
import os
import tempfile
from pathlib import Path
from rb_eit import DoubleLambdaSystem
from rb_eit.visualization import (
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


@pytest.fixture
def rb87_system():
    return DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )


@pytest.fixture
def rb85_system():
    return DoubleLambdaSystem(
        isotope="Rb85",
        pump_rabi_frequency=2 * np.pi * 15e6,
        probe_rabi_frequency=2 * np.pi * 2e6
    )


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


class TestMatplotlibPlots:
    
    def test_plot_eit_spectrum(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_spectrum.png")
        fig = plot_eit_spectrum(rb87_system, output_file=output_file, show=False)
        
        assert fig is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    
    def test_plot_comparison(self, rb87_system, temp_dir):
        system1 = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 5e6,
            probe_rabi_frequency=2 * np.pi * 1e6
        )
        system2 = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 15e6,
            probe_rabi_frequency=2 * np.pi * 1e6
        )
        
        output_file = os.path.join(temp_dir, "test_comparison.png")
        fig = plot_comparison(
            systems=[system1, system2],
            labels=['Pump: 5 MHz', 'Pump: 15 MHz'],
            output_file=output_file,
            show=False
        )
        
        assert fig is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    
    def test_plot_transmission_spectrum(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_transmission.png")
        fig = plot_transmission_spectrum(rb87_system, output_file=output_file, show=False)
        
        assert fig is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    
    def test_plot_linewidth_vs_pump_power(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_linewidth.png")
        fig = plot_linewidth_vs_pump_power(
            rb87_system,
            pump_rabi_range=(5e6, 30e6),
            num_points=10,
            output_file=output_file,
            show=False
        )
        
        assert fig is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    
    def test_plot_rb85_spectrum(self, rb85_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_rb85_spectrum.png")
        fig = plot_eit_spectrum(rb85_system, output_file=output_file, show=False)
        
        assert fig is not None
        assert os.path.exists(output_file)


class TestEnergyDiagrams:
    
    def test_plot_energy_level_diagram(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_energy_diagram.png")
        fig = plot_energy_level_diagram(rb87_system, output_file=output_file, show=False)
        
        assert fig is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    
    def test_plot_simple_level_diagram(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_simple_diagram.png")
        fig = plot_simple_level_diagram(rb87_system, output_file=output_file, show=False)
        
        assert fig is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    
    def test_energy_diagram_rb85(self, rb85_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_energy_rb85.png")
        fig = plot_energy_level_diagram(rb85_system, output_file=output_file, show=False)
        
        assert fig is not None
        assert os.path.exists(output_file)


class TestParameterSpace:
    
    def test_plot_detuning_rabi_heatmap(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_heatmap.png")
        fig = plot_detuning_rabi_heatmap(
            rb87_system,
            num_points=(50, 25),
            output_file=output_file,
            show=False
        )
        
        assert fig is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    
    def test_plot_3d_surface(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_3d_surface.png")
        fig = plot_3d_surface(
            rb87_system,
            num_points=(40, 20),
            output_file=output_file,
            show=False
        )
        
        assert fig is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    
    def test_plot_two_photon_resonance(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_two_photon.png")
        fig = plot_two_photon_resonance(
            rb87_system,
            num_points=(50, 50),
            output_file=output_file,
            show=False
        )
        
        assert fig is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0


class TestPlotlyInteractive:
    
    def test_create_interactive_eit_spectrum(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_interactive.html")
        fig = create_interactive_eit_spectrum(
            rb87_system,
            pump_rabi_range=(5e6, 30e6),
            probe_rabi_range=(0.5e6, 5e6),
            num_points=100,
            output_file=output_file
        )
        
        assert fig is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
        
        with open(output_file, 'r') as f:
            content = f.read()
            assert 'plotly' in content.lower()
    
    def test_create_interactive_heatmap(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_interactive_heatmap.html")
        fig = create_interactive_heatmap(
            rb87_system,
            num_points=(50, 30),
            output_file=output_file
        )
        
        assert fig is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    
    def test_create_interactive_3d_surface(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_interactive_3d.html")
        fig = create_interactive_3d_surface(
            rb87_system,
            num_points=(40, 30),
            output_file=output_file
        )
        
        assert fig is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    
    def test_create_parameter_sweep_comparison(self, temp_dir):
        system1 = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 5e6,
            probe_rabi_frequency=2 * np.pi * 1e6
        )
        system2 = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 15e6,
            probe_rabi_frequency=2 * np.pi * 1e6
        )
        
        output_file = os.path.join(temp_dir, "test_interactive_comparison.html")
        fig = create_parameter_sweep_comparison(
            systems=[system1, system2],
            labels=['Config 1', 'Config 2'],
            num_points=100,
            output_file=output_file
        )
        
        assert fig is not None
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0


class TestPlotFunctionality:
    
    def test_plot_without_output_file(self, rb87_system):
        fig = plot_eit_spectrum(rb87_system, show=False)
        assert fig is not None
    
    def test_different_detuning_ranges(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_range.png")
        fig = plot_eit_spectrum(
            rb87_system,
            detuning_range=(-50e6, 50e6),
            output_file=output_file,
            show=False
        )
        assert fig is not None
        assert os.path.exists(output_file)
    
    def test_custom_figsize(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_figsize.png")
        fig = plot_eit_spectrum(
            rb87_system,
            figsize=(12, 8),
            output_file=output_file,
            show=False
        )
        assert fig is not None
        assert os.path.exists(output_file)
    
    def test_high_resolution_plot(self, rb87_system, temp_dir):
        output_file = os.path.join(temp_dir, "test_high_res.png")
        fig = plot_eit_spectrum(
            rb87_system,
            num_points=1000,
            output_file=output_file,
            show=False
        )
        assert fig is not None
        assert os.path.exists(output_file)


class TestEdgeCases:
    
    def test_zero_pump_rabi(self, temp_dir):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 0.1e6,
            probe_rabi_frequency=2 * np.pi * 1e6
        )
        output_file = os.path.join(temp_dir, "test_low_pump.png")
        fig = plot_eit_spectrum(system, output_file=output_file, show=False)
        assert fig is not None
    
    def test_high_pump_rabi(self, temp_dir):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 100e6,
            probe_rabi_frequency=2 * np.pi * 1e6
        )
        output_file = os.path.join(temp_dir, "test_high_pump.png")
        fig = plot_eit_spectrum(system, output_file=output_file, show=False)
        assert fig is not None
    
    def test_with_detunings(self, temp_dir):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 10e6,
            probe_rabi_frequency=2 * np.pi * 1e6,
            pump_detuning=2 * np.pi * 5e6,
            probe_detuning=2 * np.pi * 2e6
        )
        output_file = os.path.join(temp_dir, "test_detuned.png")
        fig = plot_eit_spectrum(system, output_file=output_file, show=False)
        assert fig is not None
