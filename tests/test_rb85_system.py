import pytest
import numpy as np
from rb_eit import Rb85System


class TestRb85System:
    
    @pytest.fixture
    def rb85(self):
        return Rb85System()
    
    def test_initialization(self, rb85):
        assert rb85.nuclear_spin == 2.5
        assert len(rb85.ground_states) == 2
        assert len(rb85.excited_states_5p12) == 2
        assert len(rb85.excited_states_5p32) == 4
    
    def test_ground_state_labels(self, rb85):
        labels = [state.label for state in rb85.ground_states]
        assert "5S_1/2, F=2" in labels
        assert "5S_1/2, F=3" in labels
    
    def test_excited_state_5p12_labels(self, rb85):
        labels = [state.label for state in rb85.excited_states_5p12]
        assert "5P_1/2, F=2" in labels
        assert "5P_1/2, F=3" in labels
    
    def test_excited_state_5p32_labels(self, rb85):
        labels = [state.label for state in rb85.excited_states_5p32]
        assert "5P_3/2, F=1" in labels
        assert "5P_3/2, F=2" in labels
        assert "5P_3/2, F=3" in labels
        assert "5P_3/2, F=4" in labels
    
    def test_hyperfine_splitting(self, rb85):
        f2 = rb85.ground_states[0]
        f3 = rb85.ground_states[1]
        splitting = abs(f3.energy - f2.energy)
        hbar = 1.054571817e-34
        expected_splitting = hbar * 2 * np.pi * 3.035732439e9
        assert np.isclose(splitting, expected_splitting, rtol=0.01)
    
    def test_transitions_created(self, rb85):
        assert len(rb85.transitions_d1) > 0
        assert len(rb85.transitions_d2) > 0
        assert len(rb85.all_transitions) == len(rb85.transitions_d1) + len(rb85.transitions_d2)
    
    def test_decay_channels_created(self, rb85):
        assert len(rb85.decay_channels) > 0
    
    def test_get_transition(self, rb85):
        trans = rb85.get_transition("5S_1/2, F=3", "5P_3/2, F=4")
        assert trans.lower.label == "5S_1/2, F=3"
        assert trans.upper.label == "5P_3/2, F=4"
    
    def test_get_transition_not_found(self, rb85):
        with pytest.raises(ValueError, match="not found"):
            rb85.get_transition("Invalid1", "Invalid2")
    
    def test_get_level(self, rb85):
        level = rb85.get_level("5S_1/2, F=3")
        assert level.label == "5S_1/2, F=3"
    
    def test_get_level_not_found(self, rb85):
        with pytest.raises(ValueError, match="not found"):
            rb85.get_level("Invalid")
    
    def test_total_decay_rate(self, rb85):
        excited = rb85.excited_states_5p32[0]
        total_rate = rb85.total_decay_rate(excited)
        assert total_rate > 0
        expected_rate = 2 * np.pi * 6.065e6
        assert np.isclose(total_rate, expected_rate, rtol=0.1)
    
    def test_decay_branching_ratios_sum(self, rb85):
        for excited in rb85.all_excited_states:
            total_branching = 0.0
            for channel in rb85.decay_channels:
                if channel.upper == excited and channel.branching_ratio is not None:
                    total_branching += channel.branching_ratio
            
            if total_branching > 0:
                assert np.isclose(total_branching, 1.0, atol=1e-6)
    
    def test_transition_dipole_moments(self, rb85):
        for trans in rb85.all_transitions:
            assert trans.dipole_moment > 0
            assert trans.dipole_moment < 1e-27
    
    def test_energy_ordering(self, rb85):
        for ground in rb85.ground_states:
            for excited in rb85.all_excited_states:
                assert ground.energy < excited.energy
    
    def test_selection_rules(self, rb85):
        for trans in rb85.all_transitions:
            dF = abs(trans.upper.F - trans.lower.F)
            assert dF <= 1
            
            if trans.upper.F == 0 and trans.lower.F == 0:
                pytest.fail("Found forbidden F=0 to F=0 transition")
