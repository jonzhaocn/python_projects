from http.server import CGIHTTPRequestHandler, HTTPServer
# 使用http.server中的高级包可以快速的搭建好一个服务器
HOST = ''
PORT = 80
server = HTTPServer((HOST, PORT), CGIHTTPRequestHandler)
server.serve_forever()