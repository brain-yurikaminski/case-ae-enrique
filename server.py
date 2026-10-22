"""
Servidor Unificado Pontua+ (Dashboard Web + Apresentação + API do Agente Gemini)
Permite subir todo o ecossistema com um único comando: 'py server.py'
"""

import os
import sys
import json
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Importar o agente
sys.path.append(os.path.join(os.path.dirname(__file__), "agente"))
from agent import ask_agent

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class PontuaServerHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                query = data.get("query", "")
                answer = ask_agent(query)
                response_data = {"status": "success", "answer": answer}
            except Exception as e:
                response_data = {"status": "error", "error": str(e)}

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_error(404, "Not Found")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.lstrip("/")

        # Roteamento amigável
        if path == "" or path == "index.html":
            file_path = os.path.join(BASE_DIR, "entrega", "dashboard", "index.html")
        elif path.startswith("apresentacao"):
            subpath = path.replace("apresentacao", "").lstrip("/")
            if subpath == "" or subpath == "index.html":
                file_path = os.path.join(BASE_DIR, "entrega", "apresentacao", "index.html")
            else:
                file_path = os.path.join(BASE_DIR, "entrega", "apresentacao", subpath)
        elif path.startswith("lib/") or path.startswith("data/"):
            file_path = os.path.join(BASE_DIR, "entrega", "dashboard", path)
        else:
            file_path = os.path.join(BASE_DIR, path)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_response(200)
            mime, _ = mimetypes.guess_type(file_path)
            if file_path.endswith(".js"):
                mime = "application/javascript"
            elif file_path.endswith(".css"):
                mime = "text/css"
            elif file_path.endswith(".json"):
                mime = "application/json"
            elif file_path.endswith(".html"):
                mime = "text/html; charset=utf-8"
            
            self.send_header("Content-Type", mime or "application/octet-stream")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, f"Arquivo não encontrado: {path}")

def run():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, PontuaServerHandler)
    print("=" * 70)
    print(" Pontua+ Intelligence Server · Brain003 / Banco Aurora")
    print(f" Servidor ativo na porta {PORT}!")
    print(f" • Dashboard Estratégico:   http://localhost:{PORT}")
    print(f" • Apresentação Executiva: http://localhost:{PORT}/apresentacao")
    print(f" • API do Agente Gemini:   http://localhost:{PORT}/api/chat (POST)")
    print(" Pressione Ctrl+C para encerrar o servidor.")
    print("=" * 70)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")

if __name__ == "__main__":
    run()
