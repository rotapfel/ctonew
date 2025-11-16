import pytest
import numpy as np
from rb_eit import LaserField


class TestLaserField:
    
    def test_valid_laser_field(self):
        field = LaserField(
            rabi_frequency=2 * np.pi * 10e6,
            detuning=0.0
        )
        assert field.rabi_frequency == 2 * np.pi * 10e6
        assert field.detuning == 0.0
    
    def test_default_detuning(self):
        field = LaserField(rabi_frequency=2 * np.pi * 10e6)
        assert field.detuning == 0.0
    
    def test_negative_rabi_frequency(self):
        with pytest.raises(ValueError, match="Rabi frequency must be non-negative"):
            LaserField(rabi_frequency=-1e6, detuning=0.0)
    
    def test_invalid_polarization(self):
        with pytest.raises(ValueError, match="Polarization must be"):
            LaserField(
                rabi_frequency=1e6,
                detuning=0.0,
                polarization="invalid"
            )
    
    def test_valid_polarizations(self):
        for pol in ["linear", "sigma_plus", "sigma_minus", "circular"]:
            field = LaserField(
                rabi_frequency=1e6,
                detuning=0.0,
                polarization=pol
            )
            assert field.polarization == pol
    
    def test_phase_wrapping(self):
        field = LaserField(
            rabi_frequency=1e6,
            detuning=0.0,
            phase=3 * np.pi
        )
        assert 0 <= field.phase < 2 * np.pi
    
    def test_effective_rabi_frequency(self):
        field = LaserField(
            rabi_frequency=3e6,
            detuning=4e6
        )
        expected = np.sqrt((3e6)**2 + (4e6)**2)
        assert np.isclose(field.effective_rabi_frequency(), expected)
    
    def test_on_resonance_rabi_frequency(self):
        field = LaserField(
            rabi_frequency=10e6,
            detuning=5e6
        )
        assert field.on_resonance_rabi_frequency() == 10e6
    
    def test_electric_field_amplitude(self):
        field = LaserField(rabi_frequency=2 * np.pi * 10e6, detuning=0.0)
        dipole_moment = 1e-29
        e_field = field.electric_field_amplitude(dipole_moment)
        assert e_field > 0
    
    def test_get_intensity(self):
        field = LaserField(rabi_frequency=2 * np.pi * 10e6, detuning=0.0)
        dipole_moment = 1e-29
        intensity = field.get_intensity(dipole_moment)
        assert intensity > 0
    
    def test_set_and_get_intensity(self):
        field = LaserField(rabi_frequency=1e6, detuning=0.0)
        dipole_moment = 1e-29
        target_intensity = 1e3
        transition_freq = 1e15
        
        field.set_intensity(target_intensity, dipole_moment, transition_freq)
        calculated_intensity = field.get_intensity(dipole_moment)
        
        assert np.isclose(calculated_intensity, target_intensity, rtol=1e-6)
    
    def test_negative_intensity(self):
        field = LaserField(rabi_frequency=1e6, detuning=0.0)
        
        with pytest.raises(ValueError, match="Intensity must be non-negative"):
            LaserField(rabi_frequency=1e6, detuning=0.0, intensity=-1e3)
