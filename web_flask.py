from flask import Flask, request, send_from_directory, jsonify, Response
import io
from logger import Logger
from init_shared import shared_data
from utils import WebUtils
import os

app = Flask(__name__)
logger = Logger(name="web_flask.py", level=20)
web_utils = WebUtils(shared_data, logger)

class HandlerAdapter:
    def __init__(self, flask_request):
        self.request = flask_request
        self.headers = flask_request.headers
        self.rfile = io.BytesIO(flask_request.get_data() or b"")
        self.path = flask_request.path
        self.client_address = (flask_request.remote_addr or '127.0.0.1', 0)
        self._status = 200
        self._headers = []
        self.wfile = io.BytesIO()

    def send_response(self, code):
        self._status = code

    def send_header(self, key, value):
        self._headers.append((key, value))

    def end_headers(self):
        pass

    def get_response(self):
        body = self.wfile.getvalue()
        headers = {k: v for k, v in self._headers}
        # Determine content-type header if not provided
        if 'Content-type' in headers:
            content_type = headers.pop('Content-type')
        else:
            content_type = None
        resp = Response(body, status=self._status)
        for k, v in headers.items():
            resp.headers[k] = v
        if content_type:
            resp.headers['Content-Type'] = content_type
        return resp


# Static routes (serve files directly)
@app.route('/')
@app.route('/index.html')
def index():
    return send_from_directory(shared_data.webdir, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    # Protect against directory traversal
    safe_path = os.path.normpath(filename)
    if safe_path.startswith('..'):
        return ('', 404)
    return send_from_directory(shared_data.webdir, safe_path)

# Dynamic endpoints that reuse WebUtils via HandlerAdapter
@app.route('/load_config', methods=['GET'])
def load_config():
    adapter = HandlerAdapter(request)
    web_utils.serve_current_config(adapter)
    return adapter.get_response()

@app.route('/restore_default_config', methods=['GET'])
def restore_default_config():
    adapter = HandlerAdapter(request)
    web_utils.restore_default_config(adapter)
    return adapter.get_response()

@app.route('/get_web_delay', methods=['GET'])
def get_web_delay():
    return jsonify({"web_delay": shared_data.web_delay})

@app.route('/scan_wifi', methods=['GET'])
def scan_wifi():
    adapter = HandlerAdapter(request)
    web_utils.scan_wifi(adapter)
    return adapter.get_response()

@app.route('/network_data', methods=['GET'])
def network_data():
    adapter = HandlerAdapter(request)
    web_utils.serve_network_data(adapter)
    return adapter.get_response()

@app.route('/netkb_data', methods=['GET'])
def netkb_data():
    adapter = HandlerAdapter(request)
    web_utils.serve_netkb_data(adapter)
    return adapter.get_response()

@app.route('/netkb_data_json', methods=['GET'])
def netkb_data_json():
    adapter = HandlerAdapter(request)
    web_utils.serve_netkb_data_json(adapter)
    return adapter.get_response()

@app.route('/get_logs', methods=['GET'])
def get_logs():
    adapter = HandlerAdapter(request)
    web_utils.serve_logs(adapter)
    return adapter.get_response()

@app.route('/connect_wifi', methods=['POST'])
def connect_wifi():
    adapter = HandlerAdapter(request)
    web_utils.connect_wifi(adapter)
    shared_data.wifichanged = True
    return adapter.get_response()

@app.route('/disconnect_wifi', methods=['POST'])
def disconnect_wifi():
    adapter = HandlerAdapter(request)
    web_utils.disconnect_and_clear_wifi(adapter)
    return adapter.get_response()

@app.route('/clear_files', methods=['POST'])
def clear_files():
    adapter = HandlerAdapter(request)
    web_utils.clear_files(adapter)
    return adapter.get_response()

@app.route('/clear_files_light', methods=['POST'])
def clear_files_light():
    adapter = HandlerAdapter(request)
    web_utils.clear_files_light(adapter)
    return adapter.get_response()

@app.route('/reboot', methods=['POST'])
def reboot():
    adapter = HandlerAdapter(request)
    web_utils.reboot_system(adapter)
    return adapter.get_response()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    adapter = HandlerAdapter(request)
    web_utils.shutdown_system(adapter)
    return adapter.get_response()

@app.route('/restart_service', methods=['POST'])
def restart_service():
    adapter = HandlerAdapter(request)
    web_utils.restart_bjorn_service(adapter)
    return adapter.get_response()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
