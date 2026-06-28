from hvac_core import air_at, colebrook_white, DuctSizingInput, size_round_duct
import pytest

def test_air_density_at_20_degrees():
    a = air_at()
    assert a.density == pytest.approx(1.204, rel=0.01)

def test_f_factor_turbulent_zone():
    f = colebrook_white(100000, 0.0002)
    assert (0.018 <= f <= 0.022)

def test_complete_use_case():
    result = size_round_duct(DuctSizingInput(0.5, 1.0))
    assert ((0.30 <= result.diameter_m <= 0.35) and (5.0 <= result.velocity_ms <= 6.5))

def test_imposible_value_raise_error():
    with pytest.raises(ValueError):
        size_round_duct(DuctSizingInput(0.5, 300000))