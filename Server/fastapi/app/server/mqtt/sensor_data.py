import json
from fastapi import APIRouter
from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig
from server.database.raw_water_data import add_water
from server.my_config import MQTT_CONFIG
import datetime
import time

fast_mqtt = FastMQTT(config=MQTT_CONFIG)

router = APIRouter()

fast_mqtt.init_app(router)

@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    fast_mqtt.client.subscribe("/TGR_30/feedback")
    print("Connected: ", client, flags, rc, properties)

@fast_mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@fast_mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("Subscribed: ", client, mid, qos, properties)

@fast_mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ", topic, payload.decode(), qos, properties)

@fast_mqtt.subscribe("/TGR_30/feedback")
async def subscribe_to_topic(client, topic, payload, qos, properties):
    print("[/TGR_30/feedback]: Received", topic, payload.decode(), qos, properties)
    data_payload = json.loads(payload.decode())
    if ("success" in data_payload.keys() and data_payload["success"] == True):
        await add_water({
            "name": str(data_payload["name"] if "discharge_rate" in data_payload.keys() else "S1"),
            "height": float(data_payload["height"]),
            "time": time.time(),
            # "discharge_rate": float(data_payload["discharge_rate"]) if "discharge_rate" in data_payload.keys() else 0.0,
        })
    fast_mqtt.publish("/TGR_30/response", {"success":data_payload["success"], "topic": "/TGR_30/feedback", "message":payload.decode()})

@router.get("/command", response_description="Command Hardware")
async def command_Hardware():
    fast_mqtt.publish("/TGR_30/command", {"pass": "bless J.Ying CoE2", "cmd": "capture"})
    return {"topic": "/TGR_30/command", "message": {"pass": "bless J.Ying CoE2", "cmd": "capture"}}

@router.get("/hello", response_description="Hello MQTT Server")
async def hello_MQTT():
    fast_mqtt.publish("/TGR_30/hello", "Hello TGR_30!")
    return {"topic": "/TGR_30/hello", "message": "Hello TGR_30!"}
