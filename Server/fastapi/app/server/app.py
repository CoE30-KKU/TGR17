from fastapi import FastAPI
from server.mqtt.sensor_data import router as MqttRouter
from server.mockup.get_mockup import router as MockupRouter
from server.routes.water import router as WaterRouter
from server.routes.raw_water import router as RawWaterRouter
from server.routes.waters import router as MultipleWaterRouter
from server.routes.predict_water import router as PredictWaterRouter

from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
import os

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="./app/static", html=True), name="static")

app.include_router(MqttRouter, tags=["MQTT"], prefix="/mqtt")
# app.include_router(MockupRouter, tags=["Mockup"], prefix="/mock")
app.include_router(RawWaterRouter, tags=["Raw Water"], prefix="/rawWater")
app.include_router(WaterRouter, tags=["Water"], prefix="/water")
app.include_router(MultipleWaterRouter, tags=["Water"], prefix="/waters")
app.include_router(PredictWaterRouter, tags=["Predict Water Data"], prefix="/predictWater")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title= f"[TGR2023 — See-It 2023] API Documentation (FastAPI)",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/favicon.ico"
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title= f"[TGR2023 — See-It 2023] API Documentation (ReDoc)",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url="/static/favicon.ico"
    )

@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "My REST API server!", "group": {"id": "30", "name": "See-It 2023"}}