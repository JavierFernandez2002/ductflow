from pydantic import BaseModel, Field

class SizingRequest(BaseModel):
    flow_rate_m3s: float = Field(gt=0, description="Caudal [m3/s]")
    target_pa_per_m: float = Field(gt=0, default=0.8, description="Pérdida objetivo [Pa/m]")
    air_temp_c: float = 20

class SizingResponse(BaseModel):
    diameter_m: float
    velocity_ms: float
    reynolds: float