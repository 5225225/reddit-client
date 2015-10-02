import sys
import http.server

code = ""

class handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global code
        x = self.path
        code = [x for x in x.split("&") if x.startswith("code")][0].split("=")[1]
        self.send_response(200)
        self.end_headers()
        self.close_connection = True

    def log_message(self, format, *args):
        return
        
def get_code():
    server_address = ('', 8888)
    httpd = http.server.HTTPServer(server_address, handler)
    httpd.handle_request()
    httpd.server_close()
    assert code != ""
    return code
