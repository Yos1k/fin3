import http.server
import socketserver
import datetime
import json

with open("settings.json") as file:
    settings = json.load(file)

PORT = settings["port"]
DIRECTORY = settings["directory"]
MAX_REQUEST_SIZE = settings["max_request_size"]

def handle_get_request(request):
    path = request.split(' ')[1].replace('/', './')
    file_extension = path.split(".")[-1].lower()

    allowed_extensions = ["html", "css", "js"]
    if file_extension not in allowed_extensions:
        response = "HTTP/1.1 403 Forbidden\r\n\r\n"
        response += "403 Forbidden: File type not allowed"
    else:
        try:
            with open(path, 'rb') as file:
                content = file.read()


            response = "HTTP/1.1 200 OK\r\n"
            response += "Date: {}\r\n".format(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))
            response += "Content-type: text/html; charset=utf-8\r\n"
            response += "Server: SimpleHTTPServer\r\n"
            response += "Content-length: {}\r\n".format(len(content))
            response += "Connection: close\r\n\r\n"
            response = response.encode() + content
        except FileNotFoundError:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            response += "404 Not Found: File not found"

    return response

# Создаем TCP-сокет и привязываем его к указанному порту
with socketserver.TCPServer(("0.0.0.0", PORT), http.server.SimpleHTTPRequestHandler) as server:
    server.request_queue_size = MAX_REQUEST_SIZE

    print("Сервер запущен на порту", PORT)

    def handle_request(self):
        request = self.request.recv(1024).decode()

        if request.startswith("GET"):
            response = handle_get_request(request)
            self.request.sendall(response.encode())

    server.RequestHandlerClass.handle_request = handle_request

    server.serve_forever()
