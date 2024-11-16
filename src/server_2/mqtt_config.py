import paho.mqtt.client as paho
from paho import mqtt


# Config MQTT Broker and topics
MQTT_BROKER = 'b06816acc2d0480bb20ef15a12388f08.s1.eu.hivemq.cloud'  # Cluster URL của bạn
MQTT_PORT = 8883  # Port cho kết nối TLS
MQTT_USERNAME = 'hivemq.webclient.1729218528820'  # Username của bạn
MQTT_PASSWORD = '3#QdhgDW?29c%6<GeMrU'  # Password của bạn
DEVICE_TOPIC = 'device_topic'
SERVICE_TOPIC = 'service_topic'

# Create MQTT client
mqtt_client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
mqtt_client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

received_messages = []  # Temporary memory to store received messages


# Callback function when connected to MQTT broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker\n")
        # Subscribe to both DEVICE_TOPIC and SERVICE_TOPIC
        client.subscribe([(DEVICE_TOPIC, 0), (SERVICE_TOPIC, 0)])
    else:
        print("Failed to connect with result code " + str(rc))


# Callback function when receiving messages from subscribed topics
def on_message(client, userdata, msg):
    # Process received message
    message = msg.payload.decode()
    topic = msg.topic

    if message and topic == SERVICE_TOPIC:
        print(message)
        received_messages.append({
            "topic": topic,
            "message": message
        })


# Function to initialize the MQTT client and connect to the broker
def init_mqtt():
    # Assign the callback functions
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    try:
        # Connect to the MQTT broker
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        # Start the loop to keep the connection alive and listen for messages
        mqtt_client.loop_start()
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")

    return mqtt_client, received_messages
