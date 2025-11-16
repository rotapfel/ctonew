import pytest
import numpy as np
from rb_eit import DoubleLambdaSystem, FWMSpectraCalculator


class TestFWMSpectraCalculator:
    
    @pytest.fixture
    def system(self):
        return DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 10e6,
            probe_rabi_frequency=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0
        )
    
    @pytest.fixture
    def calculator(self, system):
        return FWMSpectraCalculator(
            system=system,
            number_density=1e17,
            interaction_length=0.01
        )
    
    def test_initialization(self, calculator):
        assert calculator.number_density == 1e17
        assert calculator.interaction_length == 0.01
        assert calculator.ground_dephasing_rate == 0.0
    
    def test_excited_decay_rate_property(self, calculator):
        decay_rate = calculator.excited_decay_rate
        assert decay_rate > 0
        assert isinstance(decay_rate, float)
    
    def test_compute_chi3_spectrum_shape(self, calculator):
        probe_detuning = np.linspace(-20e6, 20e6, 50) * 2 * np.pi
        chi3_array = calculator.compute_chi3_spectrum(probe_detuning)
        
        assert len(chi3_array) == len(probe_detuning)
        assert chi3_array.dtype == complex
    
    def test_compute_chi3_spectrum_custom_params(self, calculator):
        probe_detuning = np.linspace(-20e6, 20e6, 30) * 2 * np.pi
        chi3_array = calculator.compute_chi3_spectrum(
            probe_detuning,
            pump_rabi=2 * np.pi * 15e6,
            probe_rabi=2 * np.pi * 2e6,
            pump_detuning=2 * np.pi * 5e6
        )
        
        assert len(chi3_array) == 30
    
    def test_compute_fwm_intensity_spectrum_shape(self, calculator):
        probe_detuning = np.linspace(-20e6, 20e6, 50) * 2 * np.pi
        intensity_array = calculator.compute_fwm_intensity_spectrum(
            probe_detuning
        )
        
        assert len(intensity_array) == len(probe_detuning)
        assert intensity_array.dtype == float
        assert np.all(intensity_array >= 0)
    
    def test_compute_fwm_intensity_spectrum_custom_intensity(self, calculator):
        probe_detuning = np.linspace(-20e6, 20e6, 30) * 2 * np.pi
        intensity_array = calculator.compute_fwm_intensity_spectrum(
            probe_detuning,
            pump_intensity=2e3,
            probe_intensity=2e2
        )
        
        assert len(intensity_array) == 30
    
    def test_compute_pump_power_sweep(self, calculator):
        pump_rabi_array = np.linspace(1e6, 20e6, 20) * 2 * np.pi
        
        pump_rabi_out, chi3_array, intensity_array = (
            calculator.compute_pump_power_sweep(pump_rabi_array)
        )
        
        assert len(pump_rabi_out) == len(pump_rabi_array)
        assert len(chi3_array) == len(pump_rabi_array)
        assert len(intensity_array) == len(pump_rabi_array)
        assert chi3_array.dtype == complex
        assert np.all(intensity_array >= 0)
    
    def test_compute_coupling_detuning_sweep(self, calculator):
        pump_detuning_array = np.linspace(-30e6, 30e6, 25) * 2 * np.pi
        
        pump_det_out, chi3_array, intensity_array = (
            calculator.compute_coupling_detuning_sweep(pump_detuning_array)
        )
        
        assert len(pump_det_out) == len(pump_detuning_array)
        assert len(chi3_array) == len(pump_detuning_array)
        assert len(intensity_array) == len(pump_detuning_array)
        assert chi3_array.dtype == complex
        assert np.all(intensity_array >= 0)
    
    def test_chi3_spectrum_symmetry_on_resonance(self, calculator):
        detuning_max = 20e6 * 2 * np.pi
        probe_detuning = np.linspace(-detuning_max, detuning_max, 101) * 2 * np.pi
        
        chi3_array = calculator.compute_chi3_spectrum(
            probe_detuning,
            pump_detuning=0.0
        )
        
        mid_idx = len(chi3_array) // 2
        left_half = chi3_array[:mid_idx]
        right_half = chi3_array[mid_idx+1:][::-1]
        
        assert np.allclose(
            np.abs(left_half),
            np.abs(right_half),
            rtol=0.1
        )
    
    def test_fwm_intensity_peak_at_resonance(self, calculator):
        probe_detuning = np.linspace(-10e6, 10e6, 100) * 2 * np.pi
        intensity_array = calculator.compute_fwm_intensity_spectrum(
            probe_detuning,
            pump_detuning=0.0
        )
        
        center_idx = len(intensity_array) // 2
        center_value = intensity_array[center_idx]
        
        peak_idx = np.argmax(intensity_array)
        assert abs(peak_idx - center_idx) < 10
    
    def test_different_number_density(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        
        calc_low = FWMSpectraCalculator(system, number_density=1e16)
        calc_high = FWMSpectraCalculator(system, number_density=1e17)
        
        probe_detuning = np.array([0.0])
        
        chi3_low = calc_low.compute_chi3_spectrum(probe_detuning)[0]
        chi3_high = calc_high.compute_chi3_spectrum(probe_detuning)[0]
        
        assert np.isclose(abs(chi3_high), 10 * abs(chi3_low), rtol=0.01)
    
    def test_different_interaction_length(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        
        calc_short = FWMSpectraCalculator(system, interaction_length=0.01)
        calc_long = FWMSpectraCalculator(system, interaction_length=0.02)
        
        probe_detuning = np.array([0.0])
        
        intensity_short = calc_short.compute_fwm_intensity_spectrum(
            probe_detuning
        )[0]
        intensity_long = calc_long.compute_fwm_intensity_spectrum(
            probe_detuning
        )[0]
        
        assert np.isclose(intensity_long, 4 * intensity_short, rtol=0.01)


class TestRb85FWMSpectra:
    
    def test_rb85_system(self):
        system = DoubleLambdaSystem(
            isotope="Rb85",
            pump_rabi_frequency=2 * np.pi * 15e6,
            probe_rabi_frequency=2 * np.pi * 2e6
        )
        
        calculator = FWMSpectraCalculator(system)
        
        probe_detuning = np.linspace(-20e6, 20e6, 40) * 2 * np.pi
        chi3_array = calculator.compute_chi3_spectrum(probe_detuning)
        
        assert len(chi3_array) == 40
        assert chi3_array.dtype == complex
    
    def test_rb85_intensity_spectrum(self):
        system = DoubleLambdaSystem(isotope="Rb85")
        calculator = FWMSpectraCalculator(system)
        
        probe_detuning = np.linspace(-10e6, 10e6, 30) * 2 * np.pi
        intensity_array = calculator.compute_fwm_intensity_spectrum(
            probe_detuning
        )
        
        assert len(intensity_array) == 30
        assert np.all(intensity_array >= 0)
