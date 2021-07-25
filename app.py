import ast
import os
import json
from datetime import datetime
import paho.mqtt.client as mqtt
from http.server import HTTPServer, BaseHTTPRequestHandler

OWNTRACKS_HTTP_MQTT_HOST = os.getenv('OWNTRACKS_HTTP_MQTT_HOST', 'test.mosquitto.org')
OWNTRACKS_HTTP_MQTT_PORT = int(os.getenv('OWNTRACKS_HTTP_MQTT_PORT', 8883))
OWNTRACKS_HTTP_MQTT_USER = os.getenv('OWNTRACKS_HTTP_MQTT_USER', 'user')
OWNTRACKS_HTTP_MQTT_PASSWORD = os.getenv('OWNTRACKS_HTTP_MQTT_PASSWORD', 'password')
OWNTRACKS_HTTP_MQTT_CA_CERT = os.getenv('OWNTRACKS_HTTP_MQTT_CA_CERT', '/etc/ssl/certs/ca-cert-DST_Root_CA_X3.pem')
OWNTRACKS_HTTP_SERVER_PORT = int(os.getenv('OWNTRACKS_HTTP_SERVER_PORT', 58085))

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        request_headers = self.headers
        content_length = int(request_headers['Content-Length'])
        user = request_headers['X-Limit-D']
        if self.path.startswith('/pub?'):
            parse_msg(user, self.rfile.read(content_length))
            self.send_response(200)
        else:
            self.send_response(501)
        self.end_headers()

    def log_message(self, format, *args):
        # We don't need http.server to run its own log
        return

def parse_msg(user, msg):
    payload = ast.literal_eval(msg.decode('utf-8'))
    payload['user'] = user
    dt = datetime.fromtimestamp(payload['tst'])
    payload['time'] = dt.isoformat()
    client.publish(f'owntracks/{user}/999999999999', json.dumps(payload))
    print(payload)

def on_connect(client, userdata, flags, rc):
    print('connected to mqtt')

def print_vars():
    print('OWNTRACKS_HTTP_MQTT_HOST:',OWNTRACKS_HTTP_MQTT_HOST)
    print('OWNTRACKS_HTTP_MQTT_PORT:',OWNTRACKS_HTTP_MQTT_PORT)
    print('OWNTRACKS_HTTP_MQTT_USER:',OWNTRACKS_HTTP_MQTT_USER)
    print('OWNTRACKS_HTTP_MQTT_PASSWORD:',OWNTRACKS_HTTP_MQTT_PASSWORD)
    print('OWNTRACKS_HTTP_MQTT_CA_CERT:',OWNTRACKS_HTTP_MQTT_CA_CERT)
    print('OWNTRACKS_HTTP_SERVER_PORT:',OWNTRACKS_HTTP_SERVER_PORT)

def main():
    print_vars()
    server = HTTPServer(('', OWNTRACKS_HTTP_SERVER_PORT), RequestHandler)

    global client
    client = mqtt.Client()
    client.tls_set(OWNTRACKS_HTTP_MQTT_CA_CERT)
    client.username_pw_set(OWNTRACKS_HTTP_MQTT_USER, OWNTRACKS_HTTP_MQTT_PASSWORD)
    client.on_connect = on_connect
    client.connect(OWNTRACKS_HTTP_MQTT_HOST, OWNTRACKS_HTTP_MQTT_PORT, 60)
    client.loop_start()
    server.serve_forever()
    client.loop_stop()

if __name__ == "__main__":
    main()
