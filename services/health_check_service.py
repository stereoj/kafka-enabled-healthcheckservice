from flask import Flask, jsonify
import json
import logging
from kafka import KafkaProducer
from datetime import datetime

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='my-kafka:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/check_health', methods=['GET'])
def check_health():
    health_status = {
        "service_name": "MyService",
        "status": "OK",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    producer.send('health_checks_topic', health_status)
    logging.info(f"Sent health check: {health_status}")
    return jsonify(health_status)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5000)
