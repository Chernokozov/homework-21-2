from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from urllib.parse import parse_qs


class WebHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обрабатываем все GET-запросы - возвращаем contacts.html"""
        try:
            # Проверяем существование файла
            if not os.path.exists('contacts.html'):
                self.send_error(404, "File contacts.html not found")
                return

            # Читаем HTML файл
            with open('contacts.html', 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Отправляем ответ
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

            print(f"GET request handled: {self.path}")

        except Exception as e:
            print(f"Error: {e}")
            self.send_error(500, f"Server error: {str(e)}")

    def do_POST(self):
        """Обработка POST-запросов (дополнительное задание)"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Парсим данные формы
            form_data = parse_qs(post_data)

            # Выводим в консоль
            print("POST Data Received:")
            for key, values in form_data.items():
                print(f"   {key}: {', '.join(values)}")

            # Ответ пользователю
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            response = "<html><body><h1>Data received!</h1><a href='/'>Back</a></body></html>"
            self.wfile.write(response.encode('utf-8'))

        except Exception as e:
            print(f"POST Error: {e}")
            self.send_error(500, "POST processing error")


def run_server():
    """Запуск веб-сервера"""
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, WebHandler)

    print(f"Server running at http://localhost:{port}")
    print("All GET requests return contacts.html")
    print("POST requests are logged to console")
    print("Press Ctrl+C to stop the server")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.server_close()


if __name__ == '__main__':
    run_server()