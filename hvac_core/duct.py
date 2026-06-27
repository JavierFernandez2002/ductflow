"""Caso de uso: dimensionado de conductos por friccion constante"""
from __future__ import annotations
import math
from dataclasses import dataclass
from .hydraulics import reynolds, colebrook_white, pressure_loss_per_meter, solve_diameter_for_friction
from .air import air_at

@dataclass(frozen=True)
class DuctSizingInput:
    flow_rate_m3s: float               # m³/s
    target_pa_per_m: float = 0.8       # Pa/m
    air_temp_c: float = 20.0           # °C
    roughness_m: float = 0.00009       # m

@dataclass(frozen=True)
class DuctSizingResult:
    diameter_m: float                   # m
    velocity_ms: float             # m/s
    reynolds: float                     # adimensional
    friction_factor: float              # adimensional
    pressure_loss_pa_per_m: float       # Pa/m

def size_round_duct(data: DuctSizingInput) -> DuctSizingResult:
    """Dimensiona un conducto redondo por friccion constante."""
    if data.flow_rate_m3s <= 0:
        raise ValueError("El caudal debe ser mayor que cero.")
    air = air_at(data.air_temp_c)
    d = solve_diameter_for_friction(
        data.flow_rate_m3s, data.target_pa_per_m,
        air.density, air.kinematic_viscosity, data.roughness_m
    )
    area = math.pi * (d ** 2) / 4.0
    velocity = data.flow_rate_m3s / area
    re = reynolds(velocity, d, air.kinematic_viscosity)
    f = colebrook_white(re, data.roughness_m / d)
    return DuctSizingResult(d, velocity, re, f, data.target_pa_per_m)