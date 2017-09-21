import http.server
import requests

from pprint import pprint


def debug(v):
    pprint(v)


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    server_version = ""
    sys_version = ""

    def proxy_request(self):
        # Form the request
        request_data = self.read_request_data()
        self.sanitise_headers()
        response = requests.request(self.command,
                                    self.path,
                                    data=request_data,
                                    headers=self.headers)

        # Pass the response to the client
        self.passthru_status_line(response)
        self.passthru_headers(response)
        self.end_headers()
        self.wfile.write(response.content)

    def do_HEAD(self):
        self.proxy_request()

    def do_GET(self):
        self.proxy_request()

    def do_POST(self):
        self.proxy_request()

    def passthru_status_line(self, response):
        status_code = str(response.status_code).encode('ascii')
        reason = response.reason.encode('ascii')
        self.wfile.write(b'HTTP/1.1 %s %s\r\n' % (status_code, reason))

    def passthru_headers(self, response):
        for key, value in response.headers.items():
            if key == 'Content-Length':
                # The content-length headers received indicates the wrong
                # amount of bytes, but we can calculate the content length
                # from the content instance variable.
                self.send_header('Content-Length', len(response.content))
            else:
                self.send_header(key, value)

    def read_request_data(self):
        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            if content_length > 0:
                return self.rfile.read(content_length)
        return None

    def sanitise_headers(self):
        del(self.headers['Proxy-Connection'])


def run(port=8000):
    server_address = ("", port)
    httpd = http.server.HTTPServer(server_address, ProxyHandler)
    httpd.serve_forever()
