import pytest
import numpy as np
from rb_eit import AtomicLevel, DecayChannel


class TestDecayChannel:
    
    @pytest.fixture
    def ground_state(self):
        return AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0, energy=0.0)
    
    @pytest.fixture
    def excited_state(self):
        return AtomicLevel(n=5, L=1, J=0.5, F=2, mF=0, energy=1e-19)
    
    def test_valid_decay_channel(self, ground_state, excited_state):
        channel = DecayChannel(
            upper=excited_state,
            lower=ground_state,
            decay_rate=2 * np.pi * 6e6
        )
        assert channel.upper == excited_state
        assert channel.lower == ground_state
        assert channel.decay_rate == 2 * np.pi * 6e6
    
    def test_decay_with_branching_ratio(self, ground_state, excited_state):
        channel = DecayChannel(
            upper=excited_state,
            lower=ground_state,
            decay_rate=2 * np.pi * 3e6,
            branching_ratio=0.5
        )
        assert channel.branching_ratio == 0.5
    
    def test_invalid_energy_ordering(self, ground_state, excited_state):
        with pytest.raises(ValueError, match="Upper level energy must be greater than lower"):
            DecayChannel(
                upper=ground_state,
                lower=excited_state,
                decay_rate=1e6
            )
    
    def test_negative_decay_rate(self, ground_state, excited_state):
        with pytest.raises(ValueError, match="Decay rate must be non-negative"):
            DecayChannel(
                upper=excited_state,
                lower=ground_state,
                decay_rate=-1e6
            )
    
    def test_invalid_branching_ratio_high(self, ground_state, excited_state):
        with pytest.raises(ValueError, match="Branching ratio must be between 0 and 1"):
            DecayChannel(
                upper=excited_state,
                lower=ground_state,
                decay_rate=1e6,
                branching_ratio=1.5
            )
    
    def test_invalid_branching_ratio_low(self, ground_state, excited_state):
        with pytest.raises(ValueError, match="Branching ratio must be between 0 and 1"):
            DecayChannel(
                upper=excited_state,
                lower=ground_state,
                decay_rate=1e6,
                branching_ratio=-0.1
            )
    
    def test_invalid_delta_L(self):
        upper = AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0, energy=1e-19)
        lower = AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0, energy=0.0)
        
        with pytest.raises(ValueError, match="ΔL must be ±1"):
            DecayChannel(upper=upper, lower=lower, decay_rate=1e6)
    
    def test_invalid_delta_F(self):
        upper = AtomicLevel(n=5, L=1, J=0.5, F=3, mF=0, energy=1e-19)
        lower = AtomicLevel(n=5, L=0, J=0.5, F=1, mF=0, energy=0.0)
        
        with pytest.raises(ValueError, match="ΔF must be 0 or ±1"):
            DecayChannel(upper=upper, lower=lower, decay_rate=1e6)
    
    def test_equality(self, ground_state, excited_state):
        channel1 = DecayChannel(upper=excited_state, lower=ground_state, decay_rate=1e6)
        channel2 = DecayChannel(upper=excited_state, lower=ground_state, decay_rate=2e6)
        assert channel1 == channel2
    
    def test_hash(self, ground_state, excited_state):
        channel1 = DecayChannel(upper=excited_state, lower=ground_state, decay_rate=1e6)
        channel2 = DecayChannel(upper=excited_state, lower=ground_state, decay_rate=1e6)
        assert hash(channel1) == hash(channel2)
    
    def test_string_representation(self, ground_state, excited_state):
        channel = DecayChannel(
            upper=excited_state,
            lower=ground_state,
            decay_rate=2 * np.pi * 6e6,
            branching_ratio=0.5
        )
        
        str_repr = str(channel)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0
        
        repr_str = repr(channel)
        assert "DecayChannel" in repr_str
        assert "BR=" in repr_str
