from fastapi_mqtt.config import MQTTConfig

MONGODB_CONN = "mongodb://TGR_GROUP30:NJ485O@mongoDB:27017"

MQTT_CONFIG = MQTTConfig(
    host="emqx", # use `emqx` for local or else for your own host IP address
    port=1883,
    keepalive=60,
    username="TGR_GROUP30",
    password="NJ485O",
)
