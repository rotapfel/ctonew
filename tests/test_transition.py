import pytest
import numpy as np
from rb_eit import AtomicLevel, Transition


class TestTransition:
    
    @pytest.fixture
    def ground_state(self):
        return AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0, energy=0.0)
    
    @pytest.fixture
    def excited_state(self):
        return AtomicLevel(n=5, L=1, J=0.5, F=2, mF=0, energy=1e-19)
    
    def test_valid_transition(self, ground_state, excited_state):
        trans = Transition(
            lower=ground_state,
            upper=excited_state,
            dipole_moment=1e-29
        )
        assert trans.lower == ground_state
        assert trans.upper == excited_state
        assert trans.dipole_moment == 1e-29
    
    def test_frequency_calculation(self, ground_state, excited_state):
        trans = Transition(
            lower=ground_state,
            upper=excited_state,
            dipole_moment=1e-29
        )
        assert trans.frequency > 0
    
    def test_invalid_energy_ordering(self, ground_state, excited_state):
        with pytest.raises(ValueError, match="Lower level energy must be less than upper"):
            Transition(
                lower=excited_state,
                upper=ground_state,
                dipole_moment=1e-29
            )
    
    def test_invalid_delta_L(self):
        lower = AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0, energy=0.0)
        upper = AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0, energy=1e-19)
        
        with pytest.raises(ValueError, match="ΔL must be ±1"):
            Transition(lower=lower, upper=upper, dipole_moment=1e-29)
    
    def test_invalid_delta_F(self):
        lower = AtomicLevel(n=5, L=0, J=0.5, F=1, mF=0, energy=0.0)
        upper = AtomicLevel(n=5, L=1, J=0.5, F=3, mF=0, energy=1e-19)
        
        with pytest.raises(ValueError, match="ΔF must be 0 or ±1"):
            Transition(lower=lower, upper=upper, dipole_moment=1e-29)
    
    def test_forbidden_f0_to_f0(self):
        lower = AtomicLevel(n=5, L=1, J=1.5, F=0, mF=0, energy=0.0)
        upper = AtomicLevel(n=6, L=2, J=1.5, F=0, mF=0, energy=1e-19)
        
        with pytest.raises(ValueError, match="F=0 → F=0 transition is forbidden"):
            Transition(lower=lower, upper=upper, dipole_moment=1e-29)
    
    def test_negative_dipole_moment(self, ground_state, excited_state):
        with pytest.raises(ValueError, match="Dipole moment must be non-negative"):
            Transition(
                lower=ground_state,
                upper=excited_state,
                dipole_moment=-1e-29
            )
    
    def test_rabi_frequency(self, ground_state, excited_state):
        trans = Transition(
            lower=ground_state,
            upper=excited_state,
            dipole_moment=1e-29
        )
        
        e_field = 1e5
        rabi = trans.rabi_frequency(e_field)
        assert rabi > 0
    
    def test_equality(self, ground_state, excited_state):
        trans1 = Transition(lower=ground_state, upper=excited_state, dipole_moment=1e-29)
        trans2 = Transition(lower=ground_state, upper=excited_state, dipole_moment=2e-29)
        assert trans1 == trans2
    
    def test_hash(self, ground_state, excited_state):
        trans1 = Transition(lower=ground_state, upper=excited_state, dipole_moment=1e-29)
        trans2 = Transition(lower=ground_state, upper=excited_state, dipole_moment=1e-29)
        assert hash(trans1) == hash(trans2)
