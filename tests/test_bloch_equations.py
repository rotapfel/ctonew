import pytest
import numpy as np
from rb_eit import (
    solve_density_matrix_double_lambda,
    density_matrix_to_chi3_fwm,
    fwm_signal_intensity
)


class TestDensityMatrixSolver:
    
    def test_density_matrix_shape(self):
        rho = solve_density_matrix_double_lambda(
            pump_rabi=2 * np.pi * 10e6,
            probe_rabi=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6
        )
        
        assert rho.shape == (3, 3)
        assert rho.dtype == complex
    
    def test_density_matrix_trace(self):
        rho = solve_density_matrix_double_lambda(
            pump_rabi=2 * np.pi * 10e6,
            probe_rabi=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6
        )
        
        trace = np.trace(rho)
        assert np.isclose(trace, 1.0, atol=1e-6)
    
    def test_density_matrix_hermiticity(self):
        rho = solve_density_matrix_double_lambda(
            pump_rabi=2 * np.pi * 10e6,
            probe_rabi=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6
        )
        
        assert np.allclose(rho, rho.conj().T, atol=1e-8)
    
    def test_diagonal_elements_real(self):
        rho = solve_density_matrix_double_lambda(
            pump_rabi=2 * np.pi * 10e6,
            probe_rabi=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6
        )
        
        for i in range(3):
            assert np.isclose(rho[i, i].imag, 0.0, atol=1e-10)
            assert rho[i, i].real >= 0.0
    
    def test_population_bounds(self):
        rho = solve_density_matrix_double_lambda(
            pump_rabi=2 * np.pi * 10e6,
            probe_rabi=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6
        )
        
        for i in range(3):
            pop = rho[i, i].real
            assert 0.0 <= pop <= 1.0
    
    def test_weak_probe_limit(self):
        pump_rabi = 2 * np.pi * 10e6
        probe_rabi = 2 * np.pi * 0.1e6
        
        rho = solve_density_matrix_double_lambda(
            pump_rabi=pump_rabi,
            probe_rabi=probe_rabi,
            pump_detuning=0.0,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6
        )
        
        rho_ee = rho[2, 2].real
        assert rho_ee < 0.1
    
    def test_ground_dephasing(self):
        rho_no_dephasing = solve_density_matrix_double_lambda(
            pump_rabi=2 * np.pi * 10e6,
            probe_rabi=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6,
            ground_dephasing_rate=0.0
        )
        
        rho_with_dephasing = solve_density_matrix_double_lambda(
            pump_rabi=2 * np.pi * 10e6,
            probe_rabi=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6,
            ground_dephasing_rate=2 * np.pi * 10e6
        )
        
        assert not np.allclose(rho_no_dephasing, rho_with_dephasing)
    
    def test_detuning_effect(self):
        rho_resonant = solve_density_matrix_double_lambda(
            pump_rabi=2 * np.pi * 10e6,
            probe_rabi=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6
        )
        
        rho_detuned = solve_density_matrix_double_lambda(
            pump_rabi=2 * np.pi * 10e6,
            probe_rabi=2 * np.pi * 1e6,
            pump_detuning=2 * np.pi * 50e6,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6
        )
        
        coherence_resonant = abs(rho_resonant[0, 2])
        coherence_detuned = abs(rho_detuned[0, 2])
        assert coherence_resonant < 1e-20 and coherence_detuned < 1e-20 or coherence_resonant > coherence_detuned * 0.5


class TestChi3Calculation:
    
    def test_chi3_returns_complex(self):
        rho = solve_density_matrix_double_lambda(
            pump_rabi=2 * np.pi * 10e6,
            probe_rabi=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6
        )
        
        chi3 = density_matrix_to_chi3_fwm(
            rho=rho,
            probe_rabi=2 * np.pi * 1e6,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6,
            dipole_moment_probe=3.5e-29,
            number_density=1e17
        )
        
        assert isinstance(chi3, complex)
    
    def test_chi3_scales_with_density(self):
        rho = solve_density_matrix_double_lambda(
            pump_rabi=2 * np.pi * 10e6,
            probe_rabi=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6
        )
        
        chi3_low = density_matrix_to_chi3_fwm(
            rho=rho,
            probe_rabi=2 * np.pi * 1e6,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6,
            dipole_moment_probe=3.5e-29,
            number_density=1e16
        )
        
        chi3_high = density_matrix_to_chi3_fwm(
            rho=rho,
            probe_rabi=2 * np.pi * 1e6,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6,
            dipole_moment_probe=3.5e-29,
            number_density=1e17
        )
        
        assert np.isclose(abs(chi3_high), 10 * abs(chi3_low), rtol=0.01)
    
    def test_chi3_zero_denominator_handling(self):
        rho = np.zeros((3, 3), dtype=complex)
        rho[0, 0] = 1.0
        
        chi3 = density_matrix_to_chi3_fwm(
            rho=rho,
            probe_rabi=0.0,
            probe_detuning=0.0,
            excited_decay_rate=2 * np.pi * 6e6,
            dipole_moment_probe=3.5e-29,
            number_density=1e17
        )
        
        assert chi3 == 0j


class TestFWMIntensity:
    
    def test_fwm_intensity_positive(self):
        chi3 = 1e-10 + 1e-11j
        
        intensity = fwm_signal_intensity(
            chi3=chi3,
            pump_intensity=1e3,
            probe_intensity=1e2,
            interaction_length=0.01
        )
        
        assert intensity >= 0.0
    
    def test_fwm_intensity_zero_chi3(self):
        intensity = fwm_signal_intensity(
            chi3=0j,
            pump_intensity=1e3,
            probe_intensity=1e2,
            interaction_length=0.01
        )
        
        assert intensity == 0.0
    
    def test_fwm_intensity_scales_with_length_squared(self):
        chi3 = 1e-10 + 1e-11j
        
        intensity_short = fwm_signal_intensity(
            chi3=chi3,
            pump_intensity=1e3,
            probe_intensity=1e2,
            interaction_length=0.01
        )
        
        intensity_long = fwm_signal_intensity(
            chi3=chi3,
            pump_intensity=1e3,
            probe_intensity=1e2,
            interaction_length=0.02
        )
        
        assert np.isclose(intensity_long, 4 * intensity_short, rtol=0.01)
    
    def test_fwm_intensity_scales_with_pump_squared(self):
        chi3 = 1e-10 + 1e-11j
        
        intensity_low = fwm_signal_intensity(
            chi3=chi3,
            pump_intensity=1e3,
            probe_intensity=1e2,
            interaction_length=0.01
        )
        
        intensity_high = fwm_signal_intensity(
            chi3=chi3,
            pump_intensity=2e3,
            probe_intensity=1e2,
            interaction_length=0.01
        )
        
        assert np.isclose(intensity_high, 4 * intensity_low, rtol=0.01)
