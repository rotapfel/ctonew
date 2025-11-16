import pytest
import numpy as np
from rb_eit import (
    DoubleLambdaSystem,
    FWMSpectraCalculator,
    ParameterSweep,
    ParameterSweepResult
)


class TestParameterSweepResult:
    
    def test_1d_result_initialization(self):
        param_values = np.linspace(0, 10, 20)
        chi3_values = np.zeros(20, dtype=complex)
        intensity_values = np.zeros(20)
        
        result = ParameterSweepResult(
            parameter_name='test_param',
            parameter_values=param_values,
            chi3_values=chi3_values,
            intensity_values=intensity_values
        )
        
        assert result.parameter_name == 'test_param'
        assert len(result.parameter_values) == 20
        assert result.secondary_parameter_name is None
    
    def test_1d_result_with_fixed_params(self):
        result = ParameterSweepResult(
            parameter_name='probe_detuning',
            parameter_values=np.linspace(0, 10, 10),
            chi3_values=np.zeros(10, dtype=complex),
            intensity_values=np.zeros(10),
            fixed_parameters={'pump_rabi': 1e6, 'number_density': 1e17}
        )
        
        assert 'pump_rabi' in result.fixed_parameters
        assert result.fixed_parameters['number_density'] == 1e17
    
    def test_2d_result_initialization(self):
        param1_values = np.linspace(0, 10, 15)
        param2_values = np.linspace(0, 5, 10)
        chi3_values = np.zeros((15, 10), dtype=complex)
        intensity_values = np.zeros((15, 10))
        
        result = ParameterSweepResult(
            parameter_name='param1',
            parameter_values=param1_values,
            secondary_parameter_name='param2',
            secondary_parameter_values=param2_values,
            chi3_values=chi3_values,
            intensity_values=intensity_values
        )
        
        assert result.secondary_parameter_name == 'param2'
        assert result.chi3_values.shape == (15, 10)
    
    def test_1d_shape_mismatch_error(self):
        with pytest.raises(ValueError):
            ParameterSweepResult(
                parameter_name='test',
                parameter_values=np.linspace(0, 10, 20),
                chi3_values=np.zeros(15, dtype=complex),
                intensity_values=np.zeros(20)
            )
    
    def test_2d_shape_mismatch_error(self):
        with pytest.raises(ValueError):
            ParameterSweepResult(
                parameter_name='param1',
                parameter_values=np.linspace(0, 10, 15),
                secondary_parameter_name='param2',
                secondary_parameter_values=np.linspace(0, 5, 10),
                chi3_values=np.zeros((10, 15), dtype=complex),
                intensity_values=np.zeros((15, 10))
            )


class TestParameterSweep:
    
    @pytest.fixture
    def sweep(self):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=2 * np.pi * 10e6,
            probe_rabi_frequency=2 * np.pi * 1e6
        )
        calculator = FWMSpectraCalculator(system)
        return ParameterSweep(calculator)
    
    def test_sweep_initialization(self, sweep):
        assert isinstance(sweep.calculator, FWMSpectraCalculator)
    
    def test_sweep_probe_detuning(self, sweep):
        result = sweep.sweep_probe_detuning(
            probe_detuning_min=-10e6 * 2 * np.pi,
            probe_detuning_max=10e6 * 2 * np.pi,
            num_points=30
        )
        
        assert isinstance(result, ParameterSweepResult)
        assert result.parameter_name == 'probe_detuning'
        assert len(result.parameter_values) == 30
        assert len(result.chi3_values) == 30
        assert len(result.intensity_values) == 30
        assert np.all(result.intensity_values >= 0)
    
    def test_sweep_probe_detuning_with_fixed_params(self, sweep):
        result = sweep.sweep_probe_detuning(
            probe_detuning_min=-5e6 * 2 * np.pi,
            probe_detuning_max=5e6 * 2 * np.pi,
            num_points=20,
            pump_rabi=2 * np.pi * 15e6,
            pump_intensity=2e3
        )
        
        assert 'pump_rabi' in result.fixed_parameters
        assert result.fixed_parameters['pump_intensity'] == 2e3
    
    def test_sweep_pump_rabi_frequency(self, sweep):
        result = sweep.sweep_pump_rabi_frequency(
            pump_rabi_min=2 * np.pi * 5e6,
            pump_rabi_max=2 * np.pi * 20e6,
            num_points=25
        )
        
        assert result.parameter_name == 'pump_rabi_frequency'
        assert len(result.parameter_values) == 25
        assert len(result.chi3_values) == 25
        assert len(result.intensity_values) == 25
    
    def test_sweep_pump_rabi_frequency_custom_params(self, sweep):
        result = sweep.sweep_pump_rabi_frequency(
            pump_rabi_min=2 * np.pi * 1e6,
            pump_rabi_max=2 * np.pi * 10e6,
            num_points=15,
            probe_detuning=2 * np.pi * 1e6,
            pump_intensity=3e3,
            probe_intensity=3e2
        )
        
        assert 'probe_detuning' in result.fixed_parameters
        assert result.fixed_parameters['pump_intensity'] == 3e3
    
    def test_sweep_pump_detuning(self, sweep):
        result = sweep.sweep_pump_detuning(
            pump_detuning_min=-20e6 * 2 * np.pi,
            pump_detuning_max=20e6 * 2 * np.pi,
            num_points=30
        )
        
        assert result.parameter_name == 'pump_detuning'
        assert len(result.parameter_values) == 30
        assert len(result.chi3_values) == 30
    
    def test_sweep_2d_probe_detuning_pump_rabi(self, sweep):
        probe_detuning_values = np.linspace(-5e6, 5e6, 10) * 2 * np.pi
        pump_rabi_values = np.linspace(5e6, 15e6, 8) * 2 * np.pi
        
        result = sweep.sweep_2d(
            param1_name='probe_detuning',
            param1_values=probe_detuning_values,
            param2_name='pump_rabi',
            param2_values=pump_rabi_values
        )
        
        assert result.parameter_name == 'probe_detuning'
        assert result.secondary_parameter_name == 'pump_rabi'
        assert result.chi3_values.shape == (10, 8)
        assert result.intensity_values.shape == (10, 8)
        assert np.all(result.intensity_values >= 0)
    
    def test_sweep_2d_pump_rabi_pump_detuning(self, sweep):
        pump_rabi_values = np.linspace(5e6, 15e6, 6) * 2 * np.pi
        pump_detuning_values = np.linspace(-10e6, 10e6, 7) * 2 * np.pi
        
        result = sweep.sweep_2d(
            param1_name='pump_rabi_frequency',
            param1_values=pump_rabi_values,
            param2_name='pump_detuning',
            param2_values=pump_detuning_values
        )
        
        assert result.chi3_values.shape == (6, 7)
        assert result.intensity_values.shape == (6, 7)
        assert 'sweep_type' in result.metadata
        assert result.metadata['sweep_type'] == '2D'
    
    def test_sweep_2d_invalid_parameter(self, sweep):
        with pytest.raises(ValueError):
            sweep.sweep_2d(
                param1_name='invalid_param',
                param1_values=np.linspace(0, 10, 5),
                param2_name='probe_detuning',
                param2_values=np.linspace(0, 5, 5)
            )
    
    def test_metadata_populated(self, sweep):
        result = sweep.sweep_probe_detuning(
            probe_detuning_min=-10e6 * 2 * np.pi,
            probe_detuning_max=10e6 * 2 * np.pi,
            num_points=40
        )
        
        assert 'units' in result.metadata
        assert result.metadata['units'] == 'rad/s'
    
    def test_fixed_parameters_populated(self, sweep):
        result = sweep.sweep_pump_rabi_frequency(
            pump_rabi_min=2 * np.pi * 5e6,
            pump_rabi_max=2 * np.pi * 15e6,
            num_points=20
        )
        
        assert 'number_density' in result.fixed_parameters
        assert 'interaction_length' in result.fixed_parameters
        assert 'pump_intensity' in result.fixed_parameters
        assert 'probe_intensity' in result.fixed_parameters


class TestParameterSweepRb85:
    
    def test_rb85_sweep(self):
        system = DoubleLambdaSystem(
            isotope="Rb85",
            pump_rabi_frequency=2 * np.pi * 15e6,
            probe_rabi_frequency=2 * np.pi * 2e6
        )
        calculator = FWMSpectraCalculator(system)
        sweep = ParameterSweep(calculator)
        
        result = sweep.sweep_probe_detuning(
            probe_detuning_min=-15e6 * 2 * np.pi,
            probe_detuning_max=15e6 * 2 * np.pi,
            num_points=25
        )
        
        assert len(result.parameter_values) == 25
        assert np.all(result.intensity_values >= 0)
