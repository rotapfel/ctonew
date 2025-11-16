import pytest
import numpy as np
from rb_eit import AtomicLevel


class TestAtomicLevel:
    
    def test_valid_ground_state(self):
        level = AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0, energy=0.0)
        assert level.n == 5
        assert level.L == 0
        assert level.J == 0.5
        assert level.F == 2
        assert level.mF == 0
    
    def test_valid_excited_state(self):
        level = AtomicLevel(n=5, L=1, J=1.5, F=2, mF=1, energy=1e-19)
        assert level.n == 5
        assert level.L == 1
        assert level.J == 1.5
        assert level.F == 2
        assert level.mF == 1
    
    def test_invalid_n(self):
        with pytest.raises(ValueError, match="Principal quantum number n must be >= 1"):
            AtomicLevel(n=0, L=0, J=0.5, F=1, mF=0)
    
    def test_invalid_L(self):
        with pytest.raises(ValueError, match="Angular momentum L must be"):
            AtomicLevel(n=5, L=5, J=0.5, F=1, mF=0)
    
    def test_invalid_J(self):
        with pytest.raises(ValueError, match="Total angular momentum J must satisfy"):
            AtomicLevel(n=5, L=0, J=2.5, F=1, mF=0)
    
    def test_invalid_mF_range(self):
        with pytest.raises(ValueError, match="Magnetic quantum number mF must satisfy"):
            AtomicLevel(n=5, L=0, J=0.5, F=1, mF=2)
    
    def test_label_generation(self):
        level = AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0)
        assert "5S" in level.label
        assert "F=2" in level.label
    
    def test_custom_label(self):
        level = AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0, label="Custom")
        assert level.label == "Custom"
    
    def test_equality(self):
        level1 = AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0)
        level2 = AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0)
        assert level1 == level2
    
    def test_inequality(self):
        level1 = AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0)
        level2 = AtomicLevel(n=5, L=0, J=0.5, F=1, mF=0)
        assert level1 != level2
    
    def test_hash(self):
        level1 = AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0)
        level2 = AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0)
        assert hash(level1) == hash(level2)
    
    def test_string_representation(self):
        level = AtomicLevel(n=5, L=0, J=0.5, F=2, mF=0)
        str_repr = str(level)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0
