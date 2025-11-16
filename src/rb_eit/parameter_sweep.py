import numpy as np
from typing import Dict, Any, List, Tuple, Callable
from dataclasses import dataclass, field
from .fwm_spectra import FWMSpectraCalculator


@dataclass
class ParameterSweepResult:
    """
    Container for parameter sweep results.
    
    Attributes
    ----------
    parameter_name : str
        Name of the swept parameter
    parameter_values : np.ndarray
        Array of parameter values
    secondary_parameter_name : str or None
        Name of secondary swept parameter (for 2D sweeps)
    secondary_parameter_values : np.ndarray or None
        Array of secondary parameter values (for 2D sweeps)
    chi3_values : np.ndarray
        Array of χ^(3) values (complex)
    intensity_values : np.ndarray
        Array of FWM signal intensities
    fixed_parameters : Dict[str, Any]
        Dictionary of fixed parameter values
    metadata : Dict[str, Any]
        Additional metadata about the sweep
    """
    parameter_name: str
    parameter_values: np.ndarray
    chi3_values: np.ndarray
    intensity_values: np.ndarray
    fixed_parameters: Dict[str, Any] = field(default_factory=dict)
    secondary_parameter_name: str = None
    secondary_parameter_values: np.ndarray = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.secondary_parameter_name is not None:
            expected_shape = (
                len(self.parameter_values),
                len(self.secondary_parameter_values)
            )
            if self.chi3_values.shape != expected_shape:
                raise ValueError(
                    f"chi3_values shape {self.chi3_values.shape} doesn't match "
                    f"expected {expected_shape}"
                )
            if self.intensity_values.shape != expected_shape:
                raise ValueError(
                    f"intensity_values shape {self.intensity_values.shape} doesn't match "
                    f"expected {expected_shape}"
                )
        else:
            if len(self.chi3_values) != len(self.parameter_values):
                raise ValueError(
                    f"chi3_values length {len(self.chi3_values)} doesn't match "
                    f"parameter_values length {len(self.parameter_values)}"
                )
            if len(self.intensity_values) != len(self.parameter_values):
                raise ValueError(
                    f"intensity_values length {len(self.intensity_values)} doesn't match "
                    f"parameter_values length {len(self.parameter_values)}"
                )


class ParameterSweep:
    """
    Utility for performing multi-parameter sweeps of FWM spectra.
    """
    
    def __init__(self, calculator: FWMSpectraCalculator):
        """
        Initialize parameter sweep utility.
        
        Parameters
        ----------
        calculator : FWMSpectraCalculator
            FWM spectra calculator instance
        """
        self.calculator = calculator
    
    def sweep_probe_detuning(
        self,
        probe_detuning_min: float,
        probe_detuning_max: float,
        num_points: int = 100,
        pump_intensity: float = 1e3,
        probe_intensity: float = 1e2,
        **fixed_params
    ) -> ParameterSweepResult:
        """
        Sweep probe detuning and compute FWM spectra.
        
        Parameters
        ----------
        probe_detuning_min : float
            Minimum probe detuning (rad/s)
        probe_detuning_max : float
            Maximum probe detuning (rad/s)
        num_points : int, optional
            Number of points in sweep, default 100
        pump_intensity : float, optional
            Pump beam intensity (W/m²), default 1e3
        probe_intensity : float, optional
            Probe beam intensity (W/m²), default 1e2
        **fixed_params : dict
            Additional fixed parameters (pump_rabi, probe_rabi, pump_detuning)
        
        Returns
        -------
        result : ParameterSweepResult
            Sweep results
        """
        probe_detuning_array = np.linspace(
            probe_detuning_min, probe_detuning_max, num_points
        )
        
        intensity_array = self.calculator.compute_fwm_intensity_spectrum(
            probe_detuning_array=probe_detuning_array,
            pump_intensity=pump_intensity,
            probe_intensity=probe_intensity,
            **fixed_params
        )
        
        chi3_array = self.calculator.compute_chi3_spectrum(
            probe_detuning_array=probe_detuning_array,
            **fixed_params
        )
        
        fixed_parameters = {
            'pump_intensity': pump_intensity,
            'probe_intensity': probe_intensity,
            'number_density': self.calculator.number_density,
            'interaction_length': self.calculator.interaction_length,
            **fixed_params
        }
        
        return ParameterSweepResult(
            parameter_name='probe_detuning',
            parameter_values=probe_detuning_array,
            chi3_values=chi3_array,
            intensity_values=intensity_array,
            fixed_parameters=fixed_parameters,
            metadata={'units': 'rad/s'}
        )
    
    def sweep_pump_rabi_frequency(
        self,
        pump_rabi_min: float,
        pump_rabi_max: float,
        num_points: int = 50,
        probe_detuning: float = 0.0,
        pump_intensity: float = 1e3,
        probe_intensity: float = 1e2
    ) -> ParameterSweepResult:
        """
        Sweep pump Rabi frequency and compute FWM spectra.
        
        Parameters
        ----------
        pump_rabi_min : float
            Minimum pump Rabi frequency (rad/s)
        pump_rabi_max : float
            Maximum pump Rabi frequency (rad/s)
        num_points : int, optional
            Number of points in sweep, default 50
        probe_detuning : float, optional
            Probe detuning (rad/s), default 0
        pump_intensity : float, optional
            Pump beam intensity (W/m²), default 1e3
        probe_intensity : float, optional
            Probe beam intensity (W/m²), default 1e2
        
        Returns
        -------
        result : ParameterSweepResult
            Sweep results
        """
        pump_rabi_array = np.linspace(pump_rabi_min, pump_rabi_max, num_points)
        
        _, chi3_array, intensity_array = self.calculator.compute_pump_power_sweep(
            pump_rabi_array=pump_rabi_array,
            probe_detuning=probe_detuning,
            pump_intensity=pump_intensity,
            probe_intensity=probe_intensity
        )
        
        fixed_parameters = {
            'probe_detuning': probe_detuning,
            'pump_intensity': pump_intensity,
            'probe_intensity': probe_intensity,
            'number_density': self.calculator.number_density,
            'interaction_length': self.calculator.interaction_length
        }
        
        return ParameterSweepResult(
            parameter_name='pump_rabi_frequency',
            parameter_values=pump_rabi_array,
            chi3_values=chi3_array,
            intensity_values=intensity_array,
            fixed_parameters=fixed_parameters,
            metadata={'units': 'rad/s'}
        )
    
    def sweep_pump_detuning(
        self,
        pump_detuning_min: float,
        pump_detuning_max: float,
        num_points: int = 50,
        probe_detuning: float = 0.0,
        pump_intensity: float = 1e3,
        probe_intensity: float = 1e2
    ) -> ParameterSweepResult:
        """
        Sweep pump (coupling) detuning and compute FWM spectra.
        
        Parameters
        ----------
        pump_detuning_min : float
            Minimum pump detuning (rad/s)
        pump_detuning_max : float
            Maximum pump detuning (rad/s)
        num_points : int, optional
            Number of points in sweep, default 50
        probe_detuning : float, optional
            Probe detuning (rad/s), default 0
        pump_intensity : float, optional
            Pump beam intensity (W/m²), default 1e3
        probe_intensity : float, optional
            Probe beam intensity (W/m²), default 1e2
        
        Returns
        -------
        result : ParameterSweepResult
            Sweep results
        """
        pump_detuning_array = np.linspace(
            pump_detuning_min, pump_detuning_max, num_points
        )
        
        _, chi3_array, intensity_array = self.calculator.compute_coupling_detuning_sweep(
            pump_detuning_array=pump_detuning_array,
            probe_detuning=probe_detuning,
            pump_intensity=pump_intensity,
            probe_intensity=probe_intensity
        )
        
        fixed_parameters = {
            'probe_detuning': probe_detuning,
            'pump_intensity': pump_intensity,
            'probe_intensity': probe_intensity,
            'number_density': self.calculator.number_density,
            'interaction_length': self.calculator.interaction_length
        }
        
        return ParameterSweepResult(
            parameter_name='pump_detuning',
            parameter_values=pump_detuning_array,
            chi3_values=chi3_array,
            intensity_values=intensity_array,
            fixed_parameters=fixed_parameters,
            metadata={'units': 'rad/s'}
        )
    
    def sweep_2d(
        self,
        param1_name: str,
        param1_values: np.ndarray,
        param2_name: str,
        param2_values: np.ndarray,
        pump_intensity: float = 1e3,
        probe_intensity: float = 1e2
    ) -> ParameterSweepResult:
        """
        Perform 2D parameter sweep.
        
        Parameters
        ----------
        param1_name : str
            Name of first parameter ('probe_detuning', 'pump_rabi', or 'pump_detuning')
        param1_values : np.ndarray
            Values for first parameter
        param2_name : str
            Name of second parameter
        param2_values : np.ndarray
            Values for second parameter
        pump_intensity : float, optional
            Pump beam intensity (W/m²), default 1e3
        probe_intensity : float, optional
            Probe beam intensity (W/m²), default 1e2
        
        Returns
        -------
        result : ParameterSweepResult
            2D sweep results
        """
        n1 = len(param1_values)
        n2 = len(param2_values)
        
        chi3_grid = np.zeros((n1, n2), dtype=complex)
        intensity_grid = np.zeros((n1, n2))
        
        probe_rabi = self.calculator.system.probe.rabi_frequency
        dipole_moment = self.calculator.system.transition_2.dipole_moment
        
        from .bloch_equations import (
            solve_density_matrix_double_lambda,
            density_matrix_to_chi3_fwm,
            fwm_signal_intensity
        )
        
        for i, val1 in enumerate(param1_values):
            for j, val2 in enumerate(param2_values):
                params = self._build_params_dict(
                    param1_name, val1, param2_name, val2
                )
                
                rho = solve_density_matrix_double_lambda(
                    pump_rabi=params['pump_rabi'],
                    probe_rabi=params['probe_rabi'],
                    pump_detuning=params['pump_detuning'],
                    probe_detuning=params['probe_detuning'],
                    excited_decay_rate=self.calculator.excited_decay_rate,
                    ground_dephasing_rate=self.calculator.ground_dephasing_rate
                )
                
                chi3 = density_matrix_to_chi3_fwm(
                    rho=rho,
                    probe_rabi=params['probe_rabi'],
                    probe_detuning=params['probe_detuning'],
                    excited_decay_rate=self.calculator.excited_decay_rate,
                    dipole_moment_probe=dipole_moment,
                    number_density=self.calculator.number_density
                )
                
                chi3_grid[i, j] = chi3
                intensity_grid[i, j] = fwm_signal_intensity(
                    chi3=chi3,
                    pump_intensity=pump_intensity,
                    probe_intensity=probe_intensity,
                    interaction_length=self.calculator.interaction_length
                )
        
        fixed_parameters = {
            'pump_intensity': pump_intensity,
            'probe_intensity': probe_intensity,
            'number_density': self.calculator.number_density,
            'interaction_length': self.calculator.interaction_length
        }
        
        return ParameterSweepResult(
            parameter_name=param1_name,
            parameter_values=param1_values,
            secondary_parameter_name=param2_name,
            secondary_parameter_values=param2_values,
            chi3_values=chi3_grid,
            intensity_values=intensity_grid,
            fixed_parameters=fixed_parameters,
            metadata={'sweep_type': '2D'}
        )
    
    def _build_params_dict(
        self,
        param1_name: str,
        param1_value: float,
        param2_name: str,
        param2_value: float
    ) -> Dict[str, float]:
        """Build parameter dictionary for 2D sweep."""
        params = {
            'pump_rabi': self.calculator.system.pump.rabi_frequency,
            'probe_rabi': self.calculator.system.probe.rabi_frequency,
            'pump_detuning': self.calculator.system.pump.detuning,
            'probe_detuning': self.calculator.system.probe.detuning
        }
        
        param_map = {
            'probe_detuning': 'probe_detuning',
            'pump_rabi': 'pump_rabi',
            'pump_rabi_frequency': 'pump_rabi',
            'pump_detuning': 'pump_detuning',
            'coupling_detuning': 'pump_detuning'
        }
        
        if param1_name in param_map:
            params[param_map[param1_name]] = param1_value
        else:
            raise ValueError(f"Unknown parameter: {param1_name}")
        
        if param2_name in param_map:
            params[param_map[param2_name]] = param2_value
        else:
            raise ValueError(f"Unknown parameter: {param2_name}")
        
        return params
