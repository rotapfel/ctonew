import numpy as np
from typing import Optional
from .double_lambda import DoubleLambdaSystem
from .bloch_equations import (
    solve_density_matrix_double_lambda,
    density_matrix_to_chi3_fwm,
    fwm_signal_intensity
)


class FWMSpectraCalculator:
    """
    Calculator for Four-Wave Mixing (FWM) spectra in double-lambda systems.
    
    This class provides methods to compute third-order susceptibility χ^(3)
    and FWM signal intensities as functions of various system parameters.
    """
    
    def __init__(
        self,
        system: DoubleLambdaSystem,
        number_density: float = 1e17,
        interaction_length: float = 0.01,
        ground_dephasing_rate: float = 0.0
    ):
        """
        Initialize FWM spectra calculator.
        
        Parameters
        ----------
        system : DoubleLambdaSystem
            The double-lambda atomic system
        number_density : float, optional
            Atomic number density (atoms/m³), default 1e17
        interaction_length : float, optional
            Interaction length in medium (m), default 0.01 (1 cm)
        ground_dephasing_rate : float, optional
            Dephasing rate between ground states (rad/s), default 0
        """
        self.system = system
        self.number_density = number_density
        self.interaction_length = interaction_length
        self.ground_dephasing_rate = ground_dephasing_rate
        self._excited_decay_rate = None
    
    @property
    def excited_decay_rate(self) -> float:
        """Get total decay rate from excited state."""
        if self._excited_decay_rate is None:
            self._excited_decay_rate = self.system.atomic_system.total_decay_rate(
                self.system.excited_state
            )
        return self._excited_decay_rate
    
    def compute_chi3_spectrum(
        self,
        probe_detuning_array: np.ndarray,
        pump_rabi: Optional[float] = None,
        probe_rabi: Optional[float] = None,
        pump_detuning: Optional[float] = None
    ) -> np.ndarray:
        """
        Compute χ^(3) spectrum as function of probe detuning.
        
        Parameters
        ----------
        probe_detuning_array : np.ndarray
            Array of probe detuning values (rad/s)
        pump_rabi : float, optional
            Pump Rabi frequency (rad/s), uses system default if None
        probe_rabi : float, optional
            Probe Rabi frequency (rad/s), uses system default if None
        pump_detuning : float, optional
            Pump detuning (rad/s), uses system default if None
        
        Returns
        -------
        chi3_array : np.ndarray, dtype=complex
            Array of χ^(3) values
        """
        if pump_rabi is None:
            pump_rabi = self.system.pump.rabi_frequency
        if probe_rabi is None:
            probe_rabi = self.system.probe.rabi_frequency
        if pump_detuning is None:
            pump_detuning = self.system.pump.detuning
        
        chi3_array = np.zeros(len(probe_detuning_array), dtype=complex)
        dipole_moment = self.system.transition_2.dipole_moment
        
        for i, probe_det in enumerate(probe_detuning_array):
            rho = solve_density_matrix_double_lambda(
                pump_rabi=pump_rabi,
                probe_rabi=probe_rabi,
                pump_detuning=pump_detuning,
                probe_detuning=probe_det,
                excited_decay_rate=self.excited_decay_rate,
                ground_dephasing_rate=self.ground_dephasing_rate
            )
            
            chi3_array[i] = density_matrix_to_chi3_fwm(
                rho=rho,
                probe_rabi=probe_rabi,
                probe_detuning=probe_det,
                excited_decay_rate=self.excited_decay_rate,
                dipole_moment_probe=dipole_moment,
                number_density=self.number_density
            )
        
        return chi3_array
    
    def compute_fwm_intensity_spectrum(
        self,
        probe_detuning_array: np.ndarray,
        pump_intensity: float = 1e3,
        probe_intensity: float = 1e2,
        pump_rabi: Optional[float] = None,
        probe_rabi: Optional[float] = None,
        pump_detuning: Optional[float] = None
    ) -> np.ndarray:
        """
        Compute FWM signal intensity spectrum as function of probe detuning.
        
        Parameters
        ----------
        probe_detuning_array : np.ndarray
            Array of probe detuning values (rad/s)
        pump_intensity : float, optional
            Pump beam intensity (W/m²), default 1e3
        probe_intensity : float, optional
            Probe beam intensity (W/m²), default 1e2
        pump_rabi : float, optional
            Pump Rabi frequency (rad/s), uses system default if None
        probe_rabi : float, optional
            Probe Rabi frequency (rad/s), uses system default if None
        pump_detuning : float, optional
            Pump detuning (rad/s), uses system default if None
        
        Returns
        -------
        intensity_array : np.ndarray
            Array of FWM signal intensities (W/m²)
        """
        chi3_array = self.compute_chi3_spectrum(
            probe_detuning_array=probe_detuning_array,
            pump_rabi=pump_rabi,
            probe_rabi=probe_rabi,
            pump_detuning=pump_detuning
        )
        
        intensity_array = np.zeros(len(chi3_array))
        
        for i, chi3 in enumerate(chi3_array):
            intensity_array[i] = fwm_signal_intensity(
                chi3=chi3,
                pump_intensity=pump_intensity,
                probe_intensity=probe_intensity,
                interaction_length=self.interaction_length
            )
        
        return intensity_array
    
    def compute_pump_power_sweep(
        self,
        pump_rabi_array: np.ndarray,
        probe_detuning: float = 0.0,
        pump_intensity: float = 1e3,
        probe_intensity: float = 1e2
    ) -> tuple:
        """
        Sweep pump Rabi frequency and compute FWM spectra.
        
        Parameters
        ----------
        pump_rabi_array : np.ndarray
            Array of pump Rabi frequencies (rad/s)
        probe_detuning : float, optional
            Probe detuning (rad/s), default 0
        pump_intensity : float, optional
            Pump beam intensity (W/m²), default 1e3
        probe_intensity : float, optional
            Probe beam intensity (W/m²), default 1e2
        
        Returns
        -------
        pump_rabi_array : np.ndarray
            Input pump Rabi frequency array
        chi3_array : np.ndarray, dtype=complex
            Array of χ^(3) values
        intensity_array : np.ndarray
            Array of FWM signal intensities (W/m²)
        """
        chi3_array = np.zeros(len(pump_rabi_array), dtype=complex)
        intensity_array = np.zeros(len(pump_rabi_array))
        
        probe_rabi = self.system.probe.rabi_frequency
        pump_detuning = self.system.pump.detuning
        dipole_moment = self.system.transition_2.dipole_moment
        
        for i, pump_rabi in enumerate(pump_rabi_array):
            rho = solve_density_matrix_double_lambda(
                pump_rabi=pump_rabi,
                probe_rabi=probe_rabi,
                pump_detuning=pump_detuning,
                probe_detuning=probe_detuning,
                excited_decay_rate=self.excited_decay_rate,
                ground_dephasing_rate=self.ground_dephasing_rate
            )
            
            chi3 = density_matrix_to_chi3_fwm(
                rho=rho,
                probe_rabi=probe_rabi,
                probe_detuning=probe_detuning,
                excited_decay_rate=self.excited_decay_rate,
                dipole_moment_probe=dipole_moment,
                number_density=self.number_density
            )
            
            chi3_array[i] = chi3
            intensity_array[i] = fwm_signal_intensity(
                chi3=chi3,
                pump_intensity=pump_intensity,
                probe_intensity=probe_intensity,
                interaction_length=self.interaction_length
            )
        
        return pump_rabi_array, chi3_array, intensity_array
    
    def compute_coupling_detuning_sweep(
        self,
        pump_detuning_array: np.ndarray,
        probe_detuning: float = 0.0,
        pump_intensity: float = 1e3,
        probe_intensity: float = 1e2
    ) -> tuple:
        """
        Sweep pump (coupling) detuning and compute FWM spectra.
        
        Parameters
        ----------
        pump_detuning_array : np.ndarray
            Array of pump detuning values (rad/s)
        probe_detuning : float, optional
            Probe detuning (rad/s), default 0
        pump_intensity : float, optional
            Pump beam intensity (W/m²), default 1e3
        probe_intensity : float, optional
            Probe beam intensity (W/m²), default 1e2
        
        Returns
        -------
        pump_detuning_array : np.ndarray
            Input pump detuning array
        chi3_array : np.ndarray, dtype=complex
            Array of χ^(3) values
        intensity_array : np.ndarray
            Array of FWM signal intensities (W/m²)
        """
        chi3_array = np.zeros(len(pump_detuning_array), dtype=complex)
        intensity_array = np.zeros(len(pump_detuning_array))
        
        pump_rabi = self.system.pump.rabi_frequency
        probe_rabi = self.system.probe.rabi_frequency
        dipole_moment = self.system.transition_2.dipole_moment
        
        for i, pump_det in enumerate(pump_detuning_array):
            rho = solve_density_matrix_double_lambda(
                pump_rabi=pump_rabi,
                probe_rabi=probe_rabi,
                pump_detuning=pump_det,
                probe_detuning=probe_detuning,
                excited_decay_rate=self.excited_decay_rate,
                ground_dephasing_rate=self.ground_dephasing_rate
            )
            
            chi3 = density_matrix_to_chi3_fwm(
                rho=rho,
                probe_rabi=probe_rabi,
                probe_detuning=probe_detuning,
                excited_decay_rate=self.excited_decay_rate,
                dipole_moment_probe=dipole_moment,
                number_density=self.number_density
            )
            
            chi3_array[i] = chi3
            intensity_array[i] = fwm_signal_intensity(
                chi3=chi3,
                pump_intensity=pump_intensity,
                probe_intensity=probe_intensity,
                interaction_length=self.interaction_length
            )
        
        return pump_detuning_array, chi3_array, intensity_array
