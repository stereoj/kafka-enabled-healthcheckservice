from flask import Flask, jsonify
import json
import logging
from kafka import KafkaConsumer

app = Flask(__name__)
consumer = KafkaConsumer('health_checks_topic',
                         bootstrap_servers='my-kafka:9092',
                         auto_offset_reset='earliest',
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))

latest_health_check = {}

@app.route('/get_latest_health_check', methods=['GET'])
def get_latest_health_check():
    for msg in consumer:
        latest_health_check.update(msg.value)
    logging.info(f"Latest health check: {latest_health_check}")
    return jsonify(latest_health_check)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5001)
