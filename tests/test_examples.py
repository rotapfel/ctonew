"""
Test that example scripts execute successfully.

This ensures documentation examples remain up-to-date and functional.
"""

import sys
import subprocess
from pathlib import Path


def test_basic_usage_example():
    """Test that basic_usage.py runs without errors."""
    example_path = Path(__file__).parent.parent / "examples" / "basic_usage.py"
    assert example_path.exists(), f"Example file not found: {example_path}"
    
    result = subprocess.run(
        [sys.executable, str(example_path)],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    assert result.returncode == 0, f"Example failed with error:\n{result.stderr}"
    assert "All examples completed successfully!" in result.stdout


def test_visualization_example_import():
    """Test that visualization example can be imported."""
    example_path = Path(__file__).parent.parent / "examples" / "eit_spectrum_visualization.py"
    assert example_path.exists(), f"Visualization example not found: {example_path}"
    
    try:
        import matplotlib
        has_matplotlib = True
    except ImportError:
        has_matplotlib = False
    
    if has_matplotlib:
        result = subprocess.run(
            [sys.executable, "-c", 
             "import sys; sys.path.insert(0, 'src'); "
             "from examples.eit_spectrum_visualization import DoubleLambdaSystem"],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0, "Failed to import from visualization example"


def test_readme_quick_start_code():
    """Test that code snippets from README work correctly."""
    import numpy as np
    from rb_eit import DoubleLambdaSystem
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6,
        pump_detuning=0.0,
        probe_detuning=0.0
    )
    
    assert system is not None
    assert system.isotope == "Rb87"
    
    detuning_scan = np.linspace(-20e6, 20e6, 100) * 2 * np.pi
    susceptibility = system.eit_susceptibility(detuning_scan)
    
    assert len(susceptibility) == 100
    assert np.all(np.isfinite(susceptibility))


def test_readme_parameter_access():
    """Test parameter access examples from README."""
    from rb_eit import Rb87System
    
    rb87 = Rb87System()
    
    ground = rb87.get_level("5S_1/2, F=2")
    excited = rb87.get_level("5P_3/2, F=3")
    transition = rb87.get_transition("5S_1/2, F=2", "5P_3/2, F=3")
    
    assert ground.F == 2
    assert excited.F == 3
    assert transition.frequency > 0
    assert transition.wavelength > 0
    assert transition.dipole_moment > 0
    
    decay_rate = rb87.total_decay_rate(excited)
    assert decay_rate > 0
    
    linewidth_mhz = decay_rate / (2 * 3.14159 * 1e6)
    assert 5 < linewidth_mhz < 7


def test_custom_configuration():
    """Test custom configuration example."""
    import numpy as np
    from rb_eit import DoubleLambdaSystem
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        ground_state_1_label="5S_1/2, F=1",
        ground_state_2_label="5S_1/2, F=2",
        excited_state_label="5P_3/2, F=1",
        pump_rabi_frequency=2 * np.pi * 15e6,
        probe_rabi_frequency=2 * np.pi * 2e6
    )
    
    assert system.ground_state_1.F == 1
    assert system.ground_state_2.F == 2
    assert system.excited_state.F == 1


def test_rb85_system():
    """Test Rb-85 examples."""
    import numpy as np
    from rb_eit import DoubleLambdaSystem, Rb85System
    
    system = DoubleLambdaSystem(isotope="Rb85")
    assert system.isotope == "Rb85"
    
    rb85 = Rb85System()
    assert rb85.nuclear_spin == 2.5
    assert len(rb85.ground_states) == 2


def test_parameter_updates():
    """Test updating laser parameters."""
    import numpy as np
    from rb_eit import DoubleLambdaSystem
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    system.set_pump_parameters(2 * np.pi * 20e6, 2 * np.pi * 1e6)
    pump_rabi, probe_rabi = system.rabi_frequencies()
    
    assert abs(pump_rabi - 2 * np.pi * 20e6) < 1.0
    
    pump_det, probe_det = system.detunings()
    assert abs(pump_det - 2 * np.pi * 1e6) < 1.0


def test_two_photon_detuning():
    """Test two-photon detuning calculation."""
    import numpy as np
    from rb_eit import DoubleLambdaSystem
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6,
        pump_detuning=2 * np.pi * 5e6,
        probe_detuning=2 * np.pi * 2e6
    )
    
    delta_2p = system.two_photon_detuning()
    expected = 2 * np.pi * 3e6
    
    assert abs(delta_2p - expected) < 1e3


def test_susceptibility_physical_properties():
    """Test that susceptibility has expected physical properties."""
    import numpy as np
    from rb_eit import DoubleLambdaSystem
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6
    )
    
    detuning_scan = np.linspace(-50e6, 50e6, 500) * 2 * np.pi
    susceptibility = system.eit_susceptibility(detuning_scan)
    
    assert len(susceptibility) == len(detuning_scan)
    assert np.all(np.isfinite(susceptibility))
    
    absorption = np.imag(susceptibility)
    
    center_idx = len(detuning_scan) // 2
    edge_value = np.mean(np.abs(absorption[:10]))
    center_value = np.abs(absorption[center_idx])
    
    assert center_value < edge_value, "EIT should reduce absorption at center"
