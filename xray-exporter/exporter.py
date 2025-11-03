#!/usr/bin/env python3
import socket
import json
import time
import struct
from http.server import HTTPServer, BaseHTTPRequestHandler

XRAY_HOST = "xray"
XRAY_PORT = 10085

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            metrics = self.get_xray_metrics()
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(metrics.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def get_xray_metrics(self):
        return """# Xray metrics from logs - use Loki/Promtail for detailed analysis
xray_up 1
"""

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 9550), MetricsHandler)
    print('Starting xray exporter on port 9550')
    server.serve_forever()
