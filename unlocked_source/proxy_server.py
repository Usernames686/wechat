import os
import uvicorn
import asyncio
import httpx
import websockets
from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
def start_proxy_server(port, target_port, frontend_path):
    """
        启动代理服务器 (支持 HTTP 和 WebSocket 转发)
        :param port: 本地监听端口（提供前端页面）
        :param target_port: 目标后端端口（RPA核心服务）
        :param frontend_path: 前端静态文件路径
        """

    app = FastAPI(title="WeRobot Proxy Server")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    TARGET_BASE_URL = f'{target_port}'
    TARGET_WS_URL = "/ws"
    print("Starting Proxy Server on port ", f'{port}')
    print("- API forwarding to ", f'{TARGET_BASE_URL}')
    print("- WebSocket forwarding to ", f'{TARGET_WS_URL}')
    print("- Frontend serving from ", f'{frontend_path}')
    client = httpx.AsyncClient(base_url=TARGET_BASE_URL)
    shutdown_event = app.on_event("shutdown")((lambda : ...))
    websocket_proxy = app.websocket("/ws")((lambda client_ws: ...))
    proxy_middleware = app.middleware("http")((lambda request, call_next: Response(rp_resp.aread(), content=_, status_code=rp_resp.status_code, headers=dict(rp_resp.headers))))
    serve_spa = app.get("/{full_path:path}")((lambda full_path: FileResponse(file_path)))
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()
    dir_name = ("js", "css", "img", "assets", "icon")
    dir_path = os.path.join(frontend_path, dir_name)
    app.mount("/", f'{dir_name}', StaticFiles(directory=dir_path), name=dir_name)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8000)
parser.add_argument("--target-port", type=int, default=12138)
parser.add_argument("--frontend", type=str, default="./dist")
args = parser.parse_args()
start_proxy_server(args.port, args.target_port, args.frontend)
