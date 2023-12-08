from typing import Optional, List
from pydantic import BaseModel, Field

class WaterSchema(BaseModel):
    name: str = Field(...)
    day: int = Field(..., gt=0)
    height: float = Field(..., ge=0.0)
    discharge_rate: float = Field(..., ge=0.0)
    # waterfront: float = Field(..., ge=0.0)
    # waterback: float = Field(..., ge=0.0)
    # waterdrain: float = Field(..., ge=0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "M7",
                "day": 99,
                "height": 69.42,
                "discharge_rate": 0.0,
                # "waterfront": 121.1,
                # "waterback": 111.3,
                # "waterdrain": 102.4,
            }
        }

class MultipleWaterSchema(BaseModel):
    data: List[WaterSchema]

class UpdateWaterModel(BaseModel):
    name: Optional[str]
    day: Optional[int]
    height: Optional[float]
    discharge_rate: Optional[float]
    # waterfront: Optional[float]
    # waterback: Optional[float]
    # waterdrain: Optional[float]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "M7",
                "day": 99,
                "height": 69.42,
                "discharge_rate": 0.0,
                # "waterfront": 121.1,
                # "waterback": 111.3,
                # "waterdrain": 102.4,
            }
        }

def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}