import numpy as np
from typing import Tuple, Optional
from scipy.optimize import fsolve


def solve_density_matrix_double_lambda(
    pump_rabi: float,
    probe_rabi: float,
    pump_detuning: float,
    probe_detuning: float,
    excited_decay_rate: float,
    ground_dephasing_rate: float = 0.0
) -> np.ndarray:
    """
    Solve steady-state optical Bloch equations for a double-lambda system.
    
    The system has three levels: |1⟩, |2⟩ (ground states), and |e⟩ (excited state).
    Pump field couples |1⟩ ↔ |e⟩, probe field couples |2⟩ ↔ |e⟩.
    
    Parameters
    ----------
    pump_rabi : float
        Pump Rabi frequency (rad/s)
    probe_rabi : float
        Probe Rabi frequency (rad/s)
    pump_detuning : float
        Pump detuning from |1⟩ ↔ |e⟩ transition (rad/s)
    probe_detuning : float
        Probe detuning from |2⟩ ↔ |e⟩ transition (rad/s)
    excited_decay_rate : float
        Total decay rate from excited state (rad/s)
    ground_dephasing_rate : float, optional
        Dephasing rate between ground states (rad/s), default 0
    
    Returns
    -------
    rho : np.ndarray, shape (3, 3)
        Steady-state density matrix with ordering [|1⟩, |2⟩, |e⟩]
        rho[0,0] = ρ_11, rho[1,1] = ρ_22, rho[2,2] = ρ_ee
        rho[0,2] = ρ_1e, rho[1,2] = ρ_2e, rho[0,1] = ρ_12
    """
    gamma = excited_decay_rate
    gamma_g = ground_dephasing_rate
    
    omega_p = pump_rabi / 2
    omega_c = probe_rabi / 2
    delta_p = pump_detuning
    delta_c = probe_detuning
    
    def equations(x):
        rho11, rho22, rho_1e_r, rho_1e_i, rho_2e_r, rho_2e_i, rho_12_r, rho_12_i = x
        
        rho_ee = 1 - rho11 - rho22
        
        rho_1e = rho_1e_r + 1j * rho_1e_i
        rho_2e = rho_2e_r + 1j * rho_2e_i
        rho_12 = rho_12_r + 1j * rho_12_i
        
        drho11_dt = gamma * rho_ee + 1j * omega_p * (rho_1e - np.conj(rho_1e))
        
        drho22_dt = gamma * rho_ee + 1j * omega_c * (rho_2e - np.conj(rho_2e))
        
        drho_1e_dt = (
            -1j * delta_p * rho_1e - gamma / 2 * rho_1e +
            1j * omega_p * (rho11 - rho_ee) - 1j * omega_c * rho_12
        )
        
        drho_2e_dt = (
            -1j * delta_c * rho_2e - gamma / 2 * rho_2e +
            1j * omega_c * (rho22 - rho_ee) - 1j * omega_p * np.conj(rho_12)
        )
        
        drho_12_dt = (
            -gamma_g * rho_12 +
            1j * omega_p * rho_2e - 1j * omega_c * rho_1e
        )
        
        return [
            drho11_dt.real,
            drho22_dt.real,
            drho_1e_dt.real,
            drho_1e_dt.imag,
            drho_2e_dt.real,
            drho_2e_dt.imag,
            drho_12_dt.real,
            drho_12_dt.imag
        ]
    
    x0 = [0.5, 0.4, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
    
    sol = fsolve(equations, x0)
    
    rho11, rho22, rho_1e_r, rho_1e_i, rho_2e_r, rho_2e_i, rho_12_r, rho_12_i = sol
    rho_ee = 1 - rho11 - rho22
    
    rho = np.zeros((3, 3), dtype=complex)
    rho[0, 0] = rho11
    rho[1, 1] = rho22
    rho[2, 2] = rho_ee
    rho[0, 2] = rho_1e_r + 1j * rho_1e_i
    rho[2, 0] = np.conj(rho[0, 2])
    rho[1, 2] = rho_2e_r + 1j * rho_2e_i
    rho[2, 1] = np.conj(rho[1, 2])
    rho[0, 1] = rho_12_r + 1j * rho_12_i
    rho[1, 0] = np.conj(rho[0, 1])
    
    return rho


def density_matrix_to_chi3_fwm(
    rho: np.ndarray,
    probe_rabi: float,
    probe_detuning: float,
    excited_decay_rate: float,
    dipole_moment_probe: float,
    number_density: float
) -> complex:
    """
    Calculate third-order susceptibility for FWM from density matrix.
    
    For a double-lambda system, the FWM susceptibility is related to the
    coherence between ground states mediated by the excited state.
    
    Parameters
    ----------
    rho : np.ndarray, shape (3, 3)
        Density matrix from Bloch equation solver
    probe_rabi : float
        Probe Rabi frequency (rad/s)
    probe_detuning : float
        Probe detuning (rad/s)
    excited_decay_rate : float
        Excited state decay rate (rad/s)
    dipole_moment_probe : float
        Dipole moment for probe transition (C·m)
    number_density : float
        Atomic number density (atoms/m³)
    
    Returns
    -------
    chi3 : complex
        Third-order susceptibility (dimensionless)
    """
    from .constants import HBAR, EPSILON_0
    
    rho_12 = rho[0, 1]
    rho_2e = rho[1, 2]
    
    gamma = excited_decay_rate
    delta_c = probe_detuning
    omega_c = probe_rabi / 2
    
    denominator = (delta_c + 1j * gamma / 2) * omega_c
    
    if abs(denominator) < 1e-30:
        return 0j
    
    prefactor = (number_density * dipole_moment_probe**2) / (EPSILON_0 * HBAR)
    
    chi3 = prefactor * rho_12 / denominator
    
    return chi3


def fwm_signal_intensity(
    chi3: complex,
    pump_intensity: float,
    probe_intensity: float,
    interaction_length: float
) -> float:
    """
    Calculate FWM signal intensity from third-order susceptibility.
    
    Parameters
    ----------
    chi3 : complex
        Third-order susceptibility
    pump_intensity : float
        Pump beam intensity (W/m²)
    probe_intensity : float
        Probe beam intensity (W/m²)
    interaction_length : float
        Interaction length in medium (m)
    
    Returns
    -------
    intensity : float
        FWM signal intensity (W/m²)
    """
    from .constants import EPSILON_0, C
    
    chi3_eff = abs(chi3)**2
    
    intensity = (
        EPSILON_0 * C * chi3_eff * 
        pump_intensity**2 * probe_intensity * 
        interaction_length**2
    )
    
    return intensity
