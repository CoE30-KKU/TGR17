from typing import Optional
from pydantic import BaseModel, Field

class RawWaterSchema(BaseModel):
    name: str = Field(...)
    height: float = Field(..., ge=0.0)
    # discharge_rate: float = Field(..., ge=0.0)
    # waterfront: float = Field(..., ge=0.0)
    # waterback: float = Field(..., ge=0.0)
    # waterdrain: float = Field(..., ge=0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "M7",
                "height": 69.42,
                # "discharge_rate": 0.0,
                # "waterfront": 121.1,
                # "waterback": 111.3,
                # "waterdrain": 102.4,
            }
        }

class UpdateRawWaterModel(BaseModel):
    name: Optional[str]
    height: Optional[float]
    # discharge_rate: Optional[float]
    # waterfront: Optional[float]
    # waterback: Optional[float]
    # waterdrain: Optional[float]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "M7",
                "height": 69.42,
                # "discharge_rate": 0.0,
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