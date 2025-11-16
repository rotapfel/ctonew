import pytest
import numpy as np
from rb_eit import DoubleLambdaSystem, BlochSolver, TwoLevelBlochSolver


class TestTwoLevelBlochSolver:
    
    def test_two_level_steady_state_properties(self):
        omega = 2 * np.pi * 10e6
        delta = 0.0
        gamma = 2 * np.pi * 6e6
        
        solver = TwoLevelBlochSolver(
            rabi_frequency=omega,
            detuning=delta,
            decay_rate=gamma
        )
        
        rho = solver.solve_steady_state()
        
        assert rho.shape == (2, 2)
        
        validation = solver.validate_density_matrix(rho)
        assert validation['hermitian'], "Density matrix should be Hermitian"
        assert validation['trace_one'], "Density matrix trace should be 1"
        assert validation['positive_semidefinite'], "Density matrix should be positive semidefinite"
        assert validation['valid'], "Density matrix should be physically valid"
    
    def test_two_level_resonant_excitation(self):
        omega = 2 * np.pi * 10e6
        delta = 0.0
        gamma = 2 * np.pi * 6e6
        
        solver = TwoLevelBlochSolver(
            rabi_frequency=omega,
            detuning=delta,
            decay_rate=gamma
        )
        
        rho = solver.solve_steady_state()
        
        rho_ee = rho[1, 1].real
        expected_rho_ee = (omega**2 / 2) / (delta**2 + gamma**2 / 4 + omega**2 / 2)
        
        assert np.isclose(rho_ee, expected_rho_ee, rtol=1e-6)
    
    def test_two_level_weak_field_limit(self):
        omega = 2 * np.pi * 0.1e6
        delta = 0.0
        gamma = 2 * np.pi * 6e6
        
        solver = TwoLevelBlochSolver(
            rabi_frequency=omega,
            detuning=delta,
            decay_rate=gamma
        )
        
        rho = solver.solve_steady_state()
        
        rho_gg = rho[0, 0].real
        assert rho_gg > 0.99, "Ground state population should be near 1 for weak field"
    
    def test_two_level_strong_detuning(self):
        omega = 2 * np.pi * 10e6
        delta = 2 * np.pi * 100e6
        gamma = 2 * np.pi * 6e6
        
        solver = TwoLevelBlochSolver(
            rabi_frequency=omega,
            detuning=delta,
            decay_rate=gamma
        )
        
        rho = solver.solve_steady_state()
        
        rho_gg = rho[0, 0].real
        assert rho_gg > 0.95, "Ground state population should be near 1 for large detuning"
    
    def test_two_level_with_dephasing(self):
        omega = 2 * np.pi * 10e6
        delta = 0.0
        gamma = 2 * np.pi * 6e6
        gamma_deph = 2 * np.pi * 3e6
        
        solver = TwoLevelBlochSolver(
            rabi_frequency=omega,
            detuning=delta,
            decay_rate=gamma,
            dephasing_rate=gamma_deph
        )
        
        rho = solver.solve_steady_state()
        
        validation = solver.validate_density_matrix(rho)
        assert validation['valid'], "Density matrix should be valid with dephasing"
        
        rho_no_deph = TwoLevelBlochSolver(omega, delta, gamma).solve_steady_state()
        rho_ee_deph = rho[1, 1].real
        rho_ee_no_deph = rho_no_deph[1, 1].real
        assert rho_ee_deph < rho_ee_no_deph, "Dephasing should reduce excited state population slightly"


class TestBlochSolver:
    
    def test_bloch_solver_initialization(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        solver = BlochSolver(system)
        
        assert solver.system == system
        assert solver.gamma_excited > 0
        assert 'gamma_total' in solver.decay_rates
        assert 'gamma_e1' in solver.decay_rates
        assert 'gamma_e2' in solver.decay_rates
    
    def test_steady_state_density_matrix_shape(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        solver = BlochSolver(system)
        
        rho = solver.solve_steady_state()
        
        assert rho.shape == (3, 3)
    
    def test_steady_state_density_matrix_properties(self):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 10e6,
            probe_rabi_frequency=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0
        )
        solver = BlochSolver(system)
        
        rho = solver.solve_steady_state()
        
        validation = solver.validate_density_matrix(rho)
        assert validation['hermitian'], "Density matrix should be Hermitian"
        assert validation['trace_one'], f"Density matrix trace should be 1, got {np.trace(rho)}"
        assert validation['positive_semidefinite'], "Density matrix should be positive semidefinite"
        assert validation['valid'], "Density matrix should be physically valid"
    
    def test_steady_state_with_custom_probe_detuning(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        solver = BlochSolver(system)
        
        delta_probe = 2 * np.pi * 5e6
        rho = solver.solve_steady_state(probe_detuning=delta_probe)
        
        assert rho.shape == (3, 3)
        validation = solver.validate_density_matrix(rho)
        assert validation['valid'], "Density matrix should be valid with custom detuning"
    
    def test_sweep_probe_detuning(self):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 10e6,
            probe_rabi_frequency=2 * np.pi * 1e6
        )
        solver = BlochSolver(system)
        
        detuning_range = np.linspace(-20e6, 20e6, 50) * 2 * np.pi
        density_matrices, coherences = solver.sweep_probe_detuning(detuning_range)
        
        assert len(density_matrices) == len(detuning_range)
        assert len(coherences) == len(detuning_range)
        assert density_matrices.shape == (50, 3, 3)
        
        for rho in density_matrices:
            validation = solver.validate_density_matrix(rho)
            assert validation['valid'], "All density matrices in sweep should be valid"
    
    def test_sweep_probe_detuning_eit_transparency(self):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 10e6,
            probe_rabi_frequency=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0
        )
        solver = BlochSolver(system)
        
        detuning_range = np.linspace(-20e6, 20e6, 100) * 2 * np.pi
        _, coherences = solver.sweep_probe_detuning(detuning_range)
        
        assert np.all(np.isfinite(coherences)), "All coherences should be finite"
        assert len(coherences) == len(detuning_range), "Should have one coherence per detuning"
    
    def test_compute_susceptibility(self):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 10e6,
            probe_rabi_frequency=2 * np.pi * 1e6
        )
        solver = BlochSolver(system)
        
        detuning_range = np.linspace(-20e6, 20e6, 50) * 2 * np.pi
        absorption, dispersion = solver.compute_susceptibility(detuning_range)
        
        assert len(absorption) == len(detuning_range)
        assert len(dispersion) == len(detuning_range)
        assert np.all(np.isfinite(absorption))
        assert np.all(np.isfinite(dispersion))
    
    def test_numerical_stability_large_rabi(self):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 100e6,
            probe_rabi_frequency=2 * np.pi * 10e6
        )
        solver = BlochSolver(system)
        
        rho = solver.solve_steady_state()
        
        validation = solver.validate_density_matrix(rho)
        assert validation['valid'], "Solver should be stable for large Rabi frequencies"
    
    def test_numerical_stability_small_rabi(self):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 0.1e6,
            probe_rabi_frequency=2 * np.pi * 0.01e6
        )
        solver = BlochSolver(system)
        
        rho = solver.solve_steady_state()
        
        validation = solver.validate_density_matrix(rho)
        assert validation['valid'], "Solver should be stable for small Rabi frequencies"
        
        rho_11 = rho[0, 0].real
        rho_22 = rho[1, 1].real
        ground_state_population = rho_11 + rho_22
        assert ground_state_population > 0.99, "Most population should be in ground states for weak fields"
    
    def test_numerical_stability_large_detuning(self):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 10e6,
            probe_rabi_frequency=2 * np.pi * 1e6,
            pump_detuning=2 * np.pi * 100e6,
            probe_detuning=2 * np.pi * 100e6
        )
        solver = BlochSolver(system)
        
        rho = solver.solve_steady_state()
        
        validation = solver.validate_density_matrix(rho)
        assert validation['valid'], "Solver should be stable for large detunings"
    
    def test_with_dephasing(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        solver = BlochSolver(system, dephasing_rate=2 * np.pi * 1e6)
        
        rho = solver.solve_steady_state()
        
        validation = solver.validate_density_matrix(rho)
        assert validation['valid'], "Solver should work with dephasing"
    
    def test_rb85_system(self):
        system = DoubleLambdaSystem(isotope="Rb85")
        solver = BlochSolver(system)
        
        rho = solver.solve_steady_state()
        
        validation = solver.validate_density_matrix(rho)
        assert validation['valid'], "Solver should work with Rb85"
    
    def test_coherence_properties(self):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 10e6,
            probe_rabi_frequency=2 * np.pi * 1e6,
            pump_detuning=0.0,
            probe_detuning=0.0
        )
        solver = BlochSolver(system)
        
        rho = solver.solve_steady_state()
        
        rho_12 = rho[0, 1]
        rho_21 = rho[1, 0]
        assert np.isclose(rho_12, np.conj(rho_21)), "Off-diagonal elements should be complex conjugates"
        
        rho_13 = rho[0, 2]
        rho_31 = rho[2, 0]
        assert np.isclose(rho_13, np.conj(rho_31)), "Off-diagonal elements should be complex conjugates"
        
        rho_23 = rho[1, 2]
        rho_32 = rho[2, 1]
        assert np.isclose(rho_23, np.conj(rho_32)), "Off-diagonal elements should be complex conjugates"
    
    def test_populations_sum_to_one(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        solver = BlochSolver(system)
        
        rho = solver.solve_steady_state()
        
        total_population = rho[0, 0].real + rho[1, 1].real + rho[2, 2].real
        assert np.isclose(total_population, 1.0, atol=1e-6), "Populations should sum to 1"
    
    def test_excited_state_population_reasonable(self):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 10e6,
            probe_rabi_frequency=2 * np.pi * 1e6
        )
        solver = BlochSolver(system)
        
        rho = solver.solve_steady_state()
        
        rho_ee = rho[2, 2].real
        assert 0 <= rho_ee <= 1, "Excited state population should be between 0 and 1"
        assert rho_ee < 0.5, "Excited state population should be less than 50% for typical EIT parameters"
