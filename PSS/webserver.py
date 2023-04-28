import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler


class HandleRequests(SimpleHTTPRequestHandler):

    def do_GET(self):
        path = self.translate_path(self.path)
        if path.endswith('count'):
            with open(path, 'rb') as f:
                count_dict = json.load(f)
                value = (count_dict['value'])
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(("value = " + str(value)).encode("utf-8"))
        else:
            self.send_response(200, "OK")
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("received get request".encode("utf-8"))

    def do_PUT(self):
        path = self.translate_path(self.path)
        if path.endswith('/'):
            self.send_response(405, "Method Not Allowed")
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("PUT not allowed on a directory\n".encode())
        else:
            try:
                os.makedirs(os.path.dirname(path))
            except FileExistsError:
                pass
            length = int(self.headers['Content-Length'])
            with open(path, 'wb') as f:
                f.write(self.rfile.read(length))
            self.send_response(201, "Created")
            self.end_headers()


host = "Ondra-GamePC.sembera.net"
port = 80
HTTPServer((host, port), HandleRequests).serve_forever()
