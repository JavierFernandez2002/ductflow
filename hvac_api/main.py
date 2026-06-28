from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import SizingRequest, SizingResponse
from hvac_core import DuctSizingInput, size_round_duct

app = FastAPI(title="DuctFlow API")

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/round-sizes", response_model= SizingResponse)
def round_sizes(req: SizingRequest):
    try:
        result = size_round_duct(
            DuctSizingInput(req.flow_rate_ms, req.target_pa_per_m, req.air_temp_c)
        )
    except ValueError as a:
        raise HTTPException(status_code=422, detail=str(a))
    return SizingResponse(
        diameter_m=result.diameter_m, 
        velocity_ms=result.velocity_ms, 
        reynolds=result.reynolds)