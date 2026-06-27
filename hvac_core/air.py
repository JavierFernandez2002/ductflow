from __future__ import annotations
from dataclasses import dataclass

R_AIR = 287.058  # J/(kg·K) - specific gas constant for dry air
P_ATM_STD = 101325  # Pa - standard atmospheric pressure

@dataclass(frozen=True)
class AirProperties:
    """Propiedades del aire a una temperatura y presión dadas."""

    temperature_c: float        # °C
    pressure_pa: float          # Pa
    density: float              # kg/m³
    dynamic_viscosity: float    # Pa·s (μ)

    @property
    def kinematic_viscosity(self) -> float:
        """ν = μ / ρ  [m²/s]"""
        return self.dynamic_viscosity / self.density

def _sutherland_viscosity(temperature_c: float) -> float:
    """Viscosidad dinamica del aire por la ley de Sutherland [Pa·s]."""
    t = temperature_c + 273.15  # Convertir a Kelvin
    mu_ref, t_ref, s = 1.716e-5, 273.15, 110.4  # Pa·s, K, K
    return mu_ref * (t / t_ref) ** 1.5 * (t_ref + s) / (t + s)

def air_at(temperature_c: float = 20.0, pressure_pa: float = P_ATM_STD) -> AirProperties:
    """Calcula las propiedades del aire a una temperatura y presión dadas.

    Args:
        temperature_c (float): Temperatura en °C.
        pressure_pa (float): Presión en Pa.

    Returns:
        AirProperties: Propiedades del aire.
    """
    density = pressure_pa / (R_AIR * (temperature_c + 273.15))  # kg/m³
    dynamic_viscosity = _sutherland_viscosity(temperature_c)  # Pa·s
    return AirProperties(
        temperature_c=temperature_c,
        pressure_pa=pressure_pa,
        density=density,
        dynamic_viscosity=dynamic_viscosity
    )