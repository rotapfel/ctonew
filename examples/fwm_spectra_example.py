import numpy as np
from pathlib import Path
from rb_eit import (
    DoubleLambdaSystem,
    FWMSpectraCalculator,
    ParameterSweep,
    SpectraExporter
)


def example_chi3_spectrum():
    """
    Example: Calculate χ^(3) spectrum as a function of probe detuning.
    """
    print("=" * 70)
    print("Example 1: χ^(3) Spectrum vs Probe Detuning")
    print("=" * 70)
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 10e6,
        probe_rabi_frequency=2 * np.pi * 1e6,
        pump_detuning=0.0,
        probe_detuning=0.0
    )
    
    calculator = FWMSpectraCalculator(
        system=system,
        number_density=1e17,
        interaction_length=0.01
    )
    
    probe_detuning = np.linspace(-20e6, 20e6, 100) * 2 * np.pi
    chi3_spectrum = calculator.compute_chi3_spectrum(probe_detuning)
    
    print(f"\nSystem: {system.isotope}")
    print(f"Pump Rabi frequency: {system.pump.rabi_frequency / 1e6 / 2 / np.pi:.2f} MHz")
    print(f"Probe Rabi frequency: {system.probe.rabi_frequency / 1e6 / 2 / np.pi:.2f} MHz")
    print(f"Number of points: {len(chi3_spectrum)}")
    print(f"χ^(3) at resonance: {chi3_spectrum[50]:.3e}")
    print(f"Max |χ^(3)|: {np.max(np.abs(chi3_spectrum)):.3e}")


def example_fwm_intensity_spectrum():
    """
    Example: Calculate FWM signal intensity spectrum.
    """
    print("\n" + "=" * 70)
    print("Example 2: FWM Intensity Spectrum")
    print("=" * 70)
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 15e6,
        probe_rabi_frequency=2 * np.pi * 2e6
    )
    
    calculator = FWMSpectraCalculator(
        system=system,
        number_density=5e16,
        interaction_length=0.02
    )
    
    probe_detuning = np.linspace(-15e6, 15e6, 150) * 2 * np.pi
    intensity_spectrum = calculator.compute_fwm_intensity_spectrum(
        probe_detuning,
        pump_intensity=1e3,
        probe_intensity=1e2
    )
    
    print(f"\nInteraction length: {calculator.interaction_length * 100:.2f} cm")
    print(f"Number density: {calculator.number_density:.2e} atoms/m³")
    print(f"Pump intensity: 1000 W/m²")
    print(f"Probe intensity: 100 W/m²")
    print(f"Peak FWM intensity: {np.max(intensity_spectrum):.3e} W/m²")
    print(f"Peak location: {probe_detuning[np.argmax(intensity_spectrum)] / 1e6 / 2 / np.pi:.2f} MHz")


def example_pump_power_sweep():
    """
    Example: Sweep pump Rabi frequency and observe FWM signal.
    """
    print("\n" + "=" * 70)
    print("Example 3: Pump Power Sweep")
    print("=" * 70)
    
    system = DoubleLambdaSystem(isotope="Rb87")
    calculator = FWMSpectraCalculator(system)
    sweep = ParameterSweep(calculator)
    
    result = sweep.sweep_pump_rabi_frequency(
        pump_rabi_min=2 * np.pi * 5e6,
        pump_rabi_max=2 * np.pi * 25e6,
        num_points=40,
        probe_detuning=0.0
    )
    
    print(f"\nParameter swept: {result.parameter_name}")
    print(f"Number of points: {len(result.parameter_values)}")
    print(f"Range: {result.parameter_values[0] / 1e6 / 2 / np.pi:.2f} to "
          f"{result.parameter_values[-1] / 1e6 / 2 / np.pi:.2f} MHz")
    print(f"Max FWM intensity: {np.max(result.intensity_values):.3e} W/m²")
    
    optimal_idx = np.argmax(result.intensity_values)
    optimal_rabi = result.parameter_values[optimal_idx] / 1e6 / 2 / np.pi
    print(f"Optimal pump Rabi frequency: {optimal_rabi:.2f} MHz")


def example_coupling_detuning_sweep():
    """
    Example: Sweep pump (coupling) detuning.
    """
    print("\n" + "=" * 70)
    print("Example 4: Coupling Detuning Sweep")
    print("=" * 70)
    
    system = DoubleLambdaSystem(
        isotope="Rb87",
        pump_rabi_frequency=2 * np.pi * 12e6,
        probe_rabi_frequency=2 * np.pi * 1.5e6
    )
    calculator = FWMSpectraCalculator(system)
    sweep = ParameterSweep(calculator)
    
    result = sweep.sweep_pump_detuning(
        pump_detuning_min=-30e6 * 2 * np.pi,
        pump_detuning_max=30e6 * 2 * np.pi,
        num_points=50,
        probe_detuning=0.0
    )
    
    print(f"\nParameter swept: {result.parameter_name}")
    print(f"Number of points: {len(result.parameter_values)}")
    print(f"Fixed probe detuning: {result.fixed_parameters['probe_detuning'] / 1e6 / 2 / np.pi:.2f} MHz")
    print(f"Max FWM intensity: {np.max(result.intensity_values):.3e} W/m²")


def example_2d_sweep():
    """
    Example: 2D parameter sweep (probe detuning vs pump Rabi frequency).
    """
    print("\n" + "=" * 70)
    print("Example 5: 2D Parameter Sweep")
    print("=" * 70)
    
    system = DoubleLambdaSystem(isotope="Rb87")
    calculator = FWMSpectraCalculator(system)
    sweep = ParameterSweep(calculator)
    
    probe_detuning_values = np.linspace(-10e6, 10e6, 25) * 2 * np.pi
    pump_rabi_values = np.linspace(5e6, 20e6, 20) * 2 * np.pi
    
    result = sweep.sweep_2d(
        param1_name='probe_detuning',
        param1_values=probe_detuning_values,
        param2_name='pump_rabi',
        param2_values=pump_rabi_values
    )
    
    print(f"\nPrimary parameter: {result.parameter_name}")
    print(f"Secondary parameter: {result.secondary_parameter_name}")
    print(f"Grid shape: {result.chi3_values.shape}")
    print(f"Max FWM intensity: {np.max(result.intensity_values):.3e} W/m²")
    
    max_idx = np.unravel_index(
        np.argmax(result.intensity_values),
        result.intensity_values.shape
    )
    optimal_probe_det = result.parameter_values[max_idx[0]] / 1e6 / 2 / np.pi
    optimal_pump_rabi = result.secondary_parameter_values[max_idx[1]] / 1e6 / 2 / np.pi
    print(f"Optimal point: probe detuning = {optimal_probe_det:.2f} MHz, "
          f"pump Rabi = {optimal_pump_rabi:.2f} MHz")


def example_export_csv():
    """
    Example: Export FWM spectrum to CSV file.
    """
    print("\n" + "=" * 70)
    print("Example 6: Export to CSV")
    print("=" * 70)
    
    system = DoubleLambdaSystem(isotope="Rb87")
    calculator = FWMSpectraCalculator(system)
    sweep = ParameterSweep(calculator)
    
    result = sweep.sweep_probe_detuning(
        probe_detuning_min=-15e6 * 2 * np.pi,
        probe_detuning_max=15e6 * 2 * np.pi,
        num_points=60
    )
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    csv_path = output_dir / "fwm_spectrum.csv"
    SpectraExporter.to_csv(result, str(csv_path))
    
    print(f"\nExported to: {csv_path}")
    print(f"File size: {csv_path.stat().st_size} bytes")


def example_export_json():
    """
    Example: Export FWM spectrum to JSON file.
    """
    print("\n" + "=" * 70)
    print("Example 7: Export to JSON")
    print("=" * 70)
    
    system = DoubleLambdaSystem(
        isotope="Rb85",
        pump_rabi_frequency=2 * np.pi * 15e6,
        probe_rabi_frequency=2 * np.pi * 2e6
    )
    calculator = FWMSpectraCalculator(system)
    sweep = ParameterSweep(calculator)
    
    result = sweep.sweep_pump_rabi_frequency(
        pump_rabi_min=2 * np.pi * 5e6,
        pump_rabi_max=2 * np.pi * 25e6,
        num_points=35
    )
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    json_path = output_dir / "pump_sweep.json"
    SpectraExporter.to_json(result, str(json_path))
    
    print(f"\nExported to: {json_path}")
    print(f"File size: {json_path.stat().st_size} bytes")
    
    loaded_data = SpectraExporter.from_json(str(json_path))
    print(f"Loaded data contains {len(loaded_data['parameter']['values'])} points")
    print(f"Metadata timestamp: {loaded_data['metadata']['timestamp']}")


def example_export_multiple_formats():
    """
    Example: Export to both CSV and JSON.
    """
    print("\n" + "=" * 70)
    print("Example 8: Export to Multiple Formats")
    print("=" * 70)
    
    system = DoubleLambdaSystem(isotope="Rb87")
    calculator = FWMSpectraCalculator(system)
    sweep = ParameterSweep(calculator)
    
    result = sweep.sweep_probe_detuning(
        probe_detuning_min=-20e6 * 2 * np.pi,
        probe_detuning_max=20e6 * 2 * np.pi,
        num_points=80
    )
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    base_path = output_dir / "fwm_complete"
    filepaths = SpectraExporter.export_multiple_formats(result, str(base_path))
    
    print(f"\nExported to:")
    for format_type, filepath in filepaths.items():
        print(f"  {format_type.upper()}: {filepath}")


def example_rb85_system():
    """
    Example: FWM spectra for Rb-85 system.
    """
    print("\n" + "=" * 70)
    print("Example 9: Rb-85 FWM Spectra")
    print("=" * 70)
    
    system = DoubleLambdaSystem(
        isotope="Rb85",
        ground_state_1_label="5S_1/2, F=2",
        ground_state_2_label="5S_1/2, F=3",
        excited_state_label="5P_3/2, F=3",
        pump_rabi_frequency=2 * np.pi * 15e6,
        probe_rabi_frequency=2 * np.pi * 2e6
    )
    
    calculator = FWMSpectraCalculator(
        system=system,
        number_density=1e17,
        interaction_length=0.015
    )
    
    probe_detuning = np.linspace(-25e6, 25e6, 100) * 2 * np.pi
    intensity_spectrum = calculator.compute_fwm_intensity_spectrum(probe_detuning)
    
    print(f"\nSystem: {system}")
    print(f"Number of spectral points: {len(intensity_spectrum)}")
    print(f"Peak FWM intensity: {np.max(intensity_spectrum):.3e} W/m²")


if __name__ == "__main__":
    example_chi3_spectrum()
    example_fwm_intensity_spectrum()
    example_pump_power_sweep()
    example_coupling_detuning_sweep()
    example_2d_sweep()
    example_export_csv()
    example_export_json()
    example_export_multiple_formats()
    example_rb85_system()
    
    print("\n" + "=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)
