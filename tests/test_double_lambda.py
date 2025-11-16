import pytest
import numpy as np
from rb_eit import DoubleLambdaSystem


class TestDoubleLambdaSystem:
    
    def test_rb87_default_configuration(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        assert system.isotope == "Rb87"
        assert system.ground_state_1.label == "5S_1/2, F=1"
        assert system.ground_state_2.label == "5S_1/2, F=2"
        assert system.excited_state.label == "5P_3/2, F=2"
    
    def test_rb85_default_configuration(self):
        system = DoubleLambdaSystem(isotope="Rb85")
        assert system.isotope == "Rb85"
        assert system.ground_state_1.label == "5S_1/2, F=2"
        assert system.ground_state_2.label == "5S_1/2, F=3"
        assert system.excited_state.label == "5P_3/2, F=3"
    
    def test_invalid_isotope(self):
        with pytest.raises(ValueError, match="Unknown isotope"):
            DoubleLambdaSystem(isotope="Rb86")
    
    def test_custom_levels_rb87(self):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            ground_state_1_label="5S_1/2, F=1",
            ground_state_2_label="5S_1/2, F=2",
            excited_state_label="5P_3/2, F=1"
        )
        assert system.excited_state.label == "5P_3/2, F=1"
    
    def test_custom_laser_parameters(self):
        pump_rabi = 2 * np.pi * 20e6
        probe_rabi = 2 * np.pi * 2e6
        pump_det = 2 * np.pi * 1e6
        probe_det = 2 * np.pi * 0.5e6
        
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=pump_rabi,
            probe_rabi_frequency=probe_rabi,
            pump_detuning=pump_det,
            probe_detuning=probe_det
        )
        
        assert system.pump.rabi_frequency == pump_rabi
        assert system.probe.rabi_frequency == probe_rabi
        assert system.pump.detuning == pump_det
        assert system.probe.detuning == probe_det
    
    def test_invalid_same_ground_states(self):
        with pytest.raises(ValueError, match="Ground states must be different"):
            DoubleLambdaSystem(
                isotope="Rb87",
                ground_state_1_label="5S_1/2, F=1",
                ground_state_2_label="5S_1/2, F=1"
            )
    
    def test_two_photon_detuning(self):
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_detuning=2 * np.pi * 10e6,
            probe_detuning=2 * np.pi * 5e6
        )
        
        two_photon = system.two_photon_detuning()
        expected = 2 * np.pi * 5e6
        assert np.isclose(two_photon, expected)
    
    def test_rabi_frequencies(self):
        pump_rabi = 2 * np.pi * 15e6
        probe_rabi = 2 * np.pi * 3e6
        
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_rabi_frequency=pump_rabi,
            probe_rabi_frequency=probe_rabi
        )
        
        pump_out, probe_out = system.rabi_frequencies()
        assert pump_out == pump_rabi
        assert probe_out == probe_rabi
    
    def test_detunings(self):
        pump_det = 2 * np.pi * 2e6
        probe_det = 2 * np.pi * 1e6
        
        system = DoubleLambdaSystem(
            isotope="Rb87",
            pump_detuning=pump_det,
            probe_detuning=probe_det
        )
        
        pump_out, probe_out = system.detunings()
        assert pump_out == pump_det
        assert probe_out == probe_det
    
    def test_set_pump_parameters(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        
        new_rabi = 2 * np.pi * 25e6
        new_det = 2 * np.pi * 3e6
        
        system.set_pump_parameters(new_rabi, new_det)
        
        assert system.pump.rabi_frequency == new_rabi
        assert system.pump.detuning == new_det
    
    def test_set_probe_parameters(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        
        new_rabi = 2 * np.pi * 5e6
        new_det = 2 * np.pi * 0.5e6
        
        system.set_probe_parameters(new_rabi, new_det)
        
        assert system.probe.rabi_frequency == new_rabi
        assert system.probe.detuning == new_det
    
    def test_eit_susceptibility(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        
        detuning_scan = np.linspace(-50e6, 50e6, 100) * 2 * np.pi
        susceptibility = system.eit_susceptibility(detuning_scan)
        
        assert len(susceptibility) == len(detuning_scan)
        assert np.all(np.isfinite(susceptibility))
    
    def test_transitions_accessible(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        
        assert system.transition_1 is not None
        assert system.transition_2 is not None
        assert system.transition_1.lower == system.ground_state_1
        assert system.transition_2.lower == system.ground_state_2
        assert system.transition_1.upper == system.excited_state
        assert system.transition_2.upper == system.excited_state
    
    def test_string_representation(self):
        system = DoubleLambdaSystem(isotope="Rb87")
        
        str_repr = str(system)
        assert "Double-Lambda" in str_repr
        assert "Rb87" in str_repr
        
        repr_str = repr(system)
        assert "DoubleLambdaSystem" in repr_str
