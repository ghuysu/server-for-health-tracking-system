import paho.mqtt.client as paho
from paho import mqtt
from src.server_1.model_config import predict_health_status
import json

# Config MQTT Broker and topics
MQTT_BROKER = 'b06816acc2d0480bb20ef15a12388f08.s1.eu.hivemq.cloud'
MQTT_PORT = 8883
MQTT_USERNAME = 'hivemq.webclient.1729218528820'
MQTT_PASSWORD = '3#QdhgDW?29c%6<GeMrU'
DEVICE_TOPIC = 'device_topic'
SERVICE_TOPIC = 'service_topic'

# Create MQTT client
mqtt_client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
mqtt_client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker\n")
        client.subscribe([
            (DEVICE_TOPIC, 0),
            (SERVICE_TOPIC, 0)
        ])
    else:
        print("Failed to connect with result code " + str(rc))


def on_message(client, userdata, msg, message_ref, body_parameters):
    try:
        message = json.loads(msg.payload.decode())
        topic = msg.topic
        print(message)

        if topic == DEVICE_TOPIC:
            if not body_parameters.get('height') or \
                    not body_parameters.get('weight') or \
                    not body_parameters.get('age') or \
                    not body_parameters.get('sex'):
                return

            print(body_parameters)
            hr = float(message["heart_rate"])
            spo2 = float(message["spo2"])
            temp = float(message.get("temp", 95))
            print(message)

            prediction = predict_health_status(body_parameters['age'],
                                               body_parameters['weight'],
                                               body_parameters['height'],
                                               body_parameters['sex'],
                                               body_parameters['bmi'],
                                               temp,
                                               hr,
                                               spo2)

            # Gửi dữ liệu đến MQTT topic của service
            mqtt_client.publish(SERVICE_TOPIC, prediction)

            # Lưu trữ dữ liệu trong message_ref
            message_ref.push({
                "hr": hr,
                "spo2": spo2,
                "temp": temp,
                "prediction": prediction
            })
    except json.JSONDecodeError as error:
        print(error)


def init_mqtt(message_ref, body_parameters):
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg, message_ref, body_parameters)

    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
    return mqtt_client
