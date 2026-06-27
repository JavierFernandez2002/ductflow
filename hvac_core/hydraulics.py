"""Hidraulica de conductos: Reynolds, factor de friccion y perdida de carga.
Capa de dominio puro (solo `math`). Sin Scipy: Colebrook se resuleve 
por itereacion de punto fijo, robusta y sin dependencias externas
"""

from __future__ import annotations
import math

def reynolds(velocity: float, diameter: float, kinematic_viscosity: float) -> float:
    """Re = v·D / v (adimensional).    """
    return (velocity * diameter) / kinematic_viscosity

def colebrook_white(reynolds: float, relative_roughness: float) -> float:
    """Factor de fricción de Darcy. Laminar: 64/Re. Turbulento: Colebrook-White
    iterado, con semilla de Swamee-Jain.
    """
    if reynolds <= 0:
        raise ValueError("Reynolds debe ser mayor que cero.")
    if reynolds < 2300:
        return 64 / reynolds
    "Semilla de Swamee-Jain para flujo turbulento"
    f = 0.25 / (math.log10(relative_roughness / 3.7 + 5.74 / reynolds ** 0.9)) ** 2
    for _ in range(50):
        rhs = -2.0 * math.log10(relative_roughness / 3.7 + 2.51 / (reynolds * math.sqrt(f)))
        f_new = 1 / rhs ** 2
        if abs(f_new - f) < 1e-6:
            break
        f = f_new
    return f

def pressure_loss_per_meter(
        flow_rate: float, diameter:float,
        density: float, kinematic_viscosity: float,
        roughness: float) -> float:
    """Perdida de carga por metro de conducto [Pa/m] usando Darcy-Weisbach."""
    area = math.pi * (diameter ** 2) / 4.0
    velocity = flow_rate / area
    re = reynolds(velocity, diameter, kinematic_viscosity)
    f = colebrook_white(re, roughness / diameter)
    return f * (1.0 / diameter) * (density * velocity ** 2) / 2.0  # Pa/m

def solve_diameter_for_friction(
        flow_rate: float, target_pa_par_m: float,
        density: float, kinematic_viscosity: float, roughness: float,
        d_min: float = 0.03, d_max: float = 3.0, tol: float = 1e-6) -> float:
    """ Diametro [m] que produce la perdida objetivo (metodo de friccion constante),
    por biseccion. Aprovecha que Δp/L decrece monótonamente con D."""
    def residual(diameter: float) -> float:
        return pressure_loss_per_meter(flow_rate, diameter, density, kinematic_viscosity, roughness) - target_pa_par_m
    
    lo, hi = d_min, d_max
    f_lo, f_hi = residual(lo), residual(hi)
    if f_lo * f_hi > 0:
        raise ValueError("No se puede encontrar un diametro en el rango dado que cumpla la perdida objetivo.")
    for _ in range(100):
        mid = (lo + hi) / 2.0
        f_mid = residual(mid)
        if abs(f_mid) < tol or hi - lo < tol:
            return mid
        if f_lo * f_mid < 0:
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0  # Mejor estimacion final