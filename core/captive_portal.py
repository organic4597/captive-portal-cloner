import http.server
import socketserver

# Captive Portal 웹 서버를 실행하는 함수
def start_captive_portal(port=8080):
    try:
        print(f"Captive Portal 웹 서버 실행 중... 포트: {port}")
        
        # 간단한 HTTP 서버 구현 (로그인 페이지)
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"웹 서버가 {port} 포트에서 대기 중...")
            httpd.serve_forever()
    except Exception as e:
        print(f"Captive Portal 실행 중 오류 발생: {e}")
