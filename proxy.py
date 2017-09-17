import http.server
import requests

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    server_version = "CIA can #42"
    sys_version = ""


    def proxy_request(self, method):
        response = requests.request(method, self.path)
        self.passthru_status_line(response)
        self.passthru_headers(response)
        self.end_headers()
        self.wfile.write(response.content)


    def do_HEAD(self):
        print('HEAD')
        self.proxy_request('head')


    def do_GET(self):
       self.proxy_request('get') 


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


def run(port=8000):
    server_address = ("", 8000)
    httpd = http.server.HTTPServer(server_address, ProxyHandler)
    httpd.serve_forever()


