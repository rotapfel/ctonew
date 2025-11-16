import numpy as np
from scipy.linalg import solve, null_space
from scipy.optimize import fsolve
from typing import Optional, Tuple, Dict
from .double_lambda import DoubleLambdaSystem


class BlochSolver:
    
    def __init__(self, system: DoubleLambdaSystem, dephasing_rate: float = 0.0):
        self.system = system
        self.dephasing_rate = dephasing_rate
        
        self.gamma_excited = system.atomic_system.total_decay_rate(system.excited_state)
        
        self.decay_rates = self._compute_decay_rates()
        
    def _compute_decay_rates(self) -> Dict[str, float]:
        excited = self.system.excited_state
        g1 = self.system.ground_state_1
        g2 = self.system.ground_state_2
        
        gamma_e1 = 0.0
        gamma_e2 = 0.0
        
        for channel in self.system.atomic_system.decay_channels:
            if channel.upper == excited:
                if channel.lower == g1:
                    gamma_e1 = channel.decay_rate
                elif channel.lower == g2:
                    gamma_e2 = channel.decay_rate
        
        return {
            'gamma_total': self.gamma_excited,
            'gamma_e1': gamma_e1,
            'gamma_e2': gamma_e2
        }
    
    def _rhs(self, rho_flat: np.ndarray, Omega_p: float, Omega_c: float, 
             Delta_p: float, Delta_c: float, Gamma: float, Gamma_e1: float, 
             Gamma_e2: float, gamma_deph: float) -> np.ndarray:
        
        rho11, rho22, rho33, rho12_re, rho12_im, rho13_re, rho13_im, rho23_re, rho23_im = rho_flat
        
        rho12 = rho12_re + 1j * rho12_im
        rho13 = rho13_re + 1j * rho13_im
        rho23 = rho23_re + 1j * rho23_im
        
        drho11_dt = Gamma_e1 * rho33 + 1j * (Omega_p / 2) * (rho13 - np.conj(rho13))
        drho22_dt = Gamma_e2 * rho33 + 1j * (Omega_c / 2) * (rho23 - np.conj(rho23))
        drho33_dt = -Gamma * rho33 - 1j * (Omega_p / 2) * (rho13 - np.conj(rho13)) - 1j * (Omega_c / 2) * (rho23 - np.conj(rho23))
        
        drho12_dt = (1j * (Delta_p - Delta_c) - gamma_deph) * rho12 + 1j * (Omega_p / 2) * np.conj(rho23) - 1j * (Omega_c / 2) * rho13
        drho13_dt = (1j * Delta_p - Gamma / 2 - gamma_deph) * rho13 + 1j * (Omega_p / 2) * (rho33 - rho11) - 1j * (Omega_c / 2) * rho12
        drho23_dt = (1j * Delta_c - Gamma / 2 - gamma_deph) * rho23 + 1j * (Omega_c / 2) * (rho33 - rho22) - 1j * (Omega_p / 2) * rho12
        
        result = np.zeros(9)
        result[0] = drho11_dt.real
        result[1] = drho22_dt.real
        result[2] = drho33_dt.real
        result[3] = drho12_dt.real
        result[4] = drho12_dt.imag
        result[5] = drho13_dt.real
        result[6] = drho13_dt.imag
        result[7] = drho23_dt.real
        result[8] = drho23_dt.imag
        
        return result
    
    def solve_steady_state(self, probe_detuning: Optional[float] = None) -> np.ndarray:
        Omega_p = self.system.pump.rabi_frequency
        Omega_c = self.system.probe.rabi_frequency
        Delta_p = self.system.pump.detuning
        
        if probe_detuning is not None:
            Delta_c = probe_detuning
        else:
            Delta_c = self.system.probe.detuning
        
        Gamma = self.decay_rates['gamma_total']
        Gamma_e1 = self.decay_rates['gamma_e1']
        Gamma_e2 = self.decay_rates['gamma_e2']
        gamma_deph = self.dephasing_rate
        
        def equations(x):
            rho_flat = np.zeros(9)
            rho_flat[:8] = x
            rho_flat[2] = 1.0 - x[0] - x[1]
            eqs = self._rhs(rho_flat, Omega_p, Omega_c, Delta_p, Delta_c, Gamma, Gamma_e1, Gamma_e2, gamma_deph)
            return np.concatenate([eqs[:2], eqs[3:]])
        
        initial_guess = np.array([0.45, 0.45, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        
        try:
            x_solution = fsolve(equations, initial_guess, full_output=False)
            rho11 = x_solution[0]
            rho22 = x_solution[1]
            rho33 = 1.0 - rho11 - rho22
            rho12_re = x_solution[2]
            rho12_im = x_solution[3]
            rho13_re = x_solution[4]
            rho13_im = x_solution[5]
            rho23_re = x_solution[6]
            rho23_im = x_solution[7]
        except:
            rho11 = 0.45
            rho22 = 0.45
            rho33 = 0.1
            rho12_re = rho12_im = rho13_re = rho13_im = rho23_re = rho23_im = 0.0
        
        rho = np.array([
            [rho11, rho12_re + 1j * rho12_im, rho13_re + 1j * rho13_im],
            [rho12_re - 1j * rho12_im, rho22, rho23_re + 1j * rho23_im],
            [rho13_re - 1j * rho13_im, rho23_re - 1j * rho23_im, rho33]
        ], dtype=complex)
        
        rho = self._ensure_physical(rho)
        
        return rho
    
    def _ensure_physical(self, rho: np.ndarray) -> np.ndarray:
        rho = (rho + rho.conj().T) / 2
        
        trace = np.trace(rho)
        if abs(trace) > 1e-10:
            rho = rho / trace
        else:
            rho = np.eye(rho.shape[0]) / rho.shape[0]
        
        eigenvalues, eigenvectors = np.linalg.eigh(rho)
        eigenvalues = np.maximum(eigenvalues, 0)
        eigenvalues = eigenvalues / np.sum(eigenvalues)
        rho = eigenvectors @ np.diag(eigenvalues) @ eigenvectors.conj().T
        
        return rho
    
    def validate_density_matrix(self, rho: np.ndarray, tol: float = 1e-6) -> Dict[str, bool]:
        is_hermitian = np.allclose(rho, rho.conj().T, atol=tol)
        
        trace = np.trace(rho).real
        trace_is_one = np.isclose(trace, 1.0, atol=tol)
        
        eigenvalues = np.linalg.eigvalsh(rho)
        is_positive_semidefinite = np.all(eigenvalues >= -tol)
        
        return {
            'hermitian': is_hermitian,
            'trace_one': trace_is_one,
            'positive_semidefinite': is_positive_semidefinite,
            'valid': is_hermitian and trace_is_one and is_positive_semidefinite
        }
    
    def sweep_probe_detuning(
        self,
        detuning_range: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        density_matrices = []
        coherences = np.zeros(len(detuning_range), dtype=complex)
        
        for i, delta_probe in enumerate(detuning_range):
            rho = self.solve_steady_state(probe_detuning=delta_probe)
            density_matrices.append(rho)
            coherences[i] = rho[1, 2]
        
        return np.array(density_matrices), coherences
    
    def compute_susceptibility(
        self,
        detuning_range: np.ndarray,
        atom_density: float = 1e17
    ) -> Tuple[np.ndarray, np.ndarray]:
        from .constants import EPSILON_0, HBAR
        
        _, coherences = self.sweep_probe_detuning(detuning_range)
        
        dipole_moment = self.system.transition_2.dipole_moment
        
        prefactor = (atom_density * dipole_moment**2) / (2 * EPSILON_0 * HBAR)
        
        susceptibility = prefactor * coherences / self.system.probe.rabi_frequency
        
        absorption = -2 * susceptibility.imag
        dispersion = 2 * susceptibility.real
        
        return absorption, dispersion


class TwoLevelBlochSolver:
    
    def __init__(
        self,
        rabi_frequency: float,
        detuning: float,
        decay_rate: float,
        dephasing_rate: float = 0.0
    ):
        self.omega = rabi_frequency
        self.delta = detuning
        self.gamma = decay_rate
        self.gamma_deph = dephasing_rate
    
    def solve_steady_state(self) -> np.ndarray:
        omega = self.omega
        delta = self.delta
        gamma = self.gamma
        gamma_deph = self.gamma_deph
        
        denom = delta**2 + (gamma / 2 + gamma_deph)**2 + omega**2 / 2
        
        rho_ee = (omega**2 / 2) / denom
        rho_gg = 1.0 - rho_ee
        
        rho_ge = (-1j * omega / 2) * (delta - 1j * (gamma / 2 + gamma_deph)) / denom
        rho_eg = np.conj(rho_ge)
        
        rho = np.array([
            [rho_gg, rho_ge],
            [rho_eg, rho_ee]
        ], dtype=complex)
        
        return rho
    
    def validate_density_matrix(self, rho: np.ndarray, tol: float = 1e-6) -> Dict[str, bool]:
        is_hermitian = np.allclose(rho, rho.conj().T, atol=tol)
        
        trace = np.trace(rho).real
        trace_is_one = np.isclose(trace, 1.0, atol=tol)
        
        eigenvalues = np.linalg.eigvalsh(rho)
        is_positive_semidefinite = np.all(eigenvalues >= -tol)
        
        return {
            'hermitian': is_hermitian,
            'trace_one': trace_is_one,
            'positive_semidefinite': is_positive_semidefinite,
            'valid': is_hermitian and trace_is_one and is_positive_semidefinite
        }
