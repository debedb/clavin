from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import json
import socket
from typing import Dict, List, Any
from postman_client import PostmanClient
from collection_parser import CollectionParser


class MockServer:
    def __init__(self, collection_id: str, port: int = None):
        self.collection_id = collection_id
        self.port = port or self._get_free_port()
        self.app = FastAPI(title="Postman Mock Server", version="1.0.0")
        self.routes = []
        
    def _get_free_port(self) -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    def setup_routes(self):
        try:
            client = PostmanClient()
            collection_data = client.get_collection(self.collection_id)
            parser = CollectionParser(collection_data)
            self.routes = parser.parse()
        except Exception as e:
            raise Exception(f"Failed to setup routes from collection {self.collection_id}: {e}")
        
        for route in self.routes:
            self._add_route(route)
        
        print(f"Mock server setup complete with {len(self.routes)} routes")
        for route in self.routes:
            print(f"  {route['method']} {route['path']} - {route['name']}")
    
    def _add_route(self, route: Dict[str, Any]):
        method = route["method"].lower()
        path = route["path"]
        response_data = route["response"]
        
        async def endpoint_handler(request: Request):
            return self._create_response(response_data)
        
        endpoint_handler.__name__ = f"{method}_{path.replace('/', '_').replace('{', '').replace('}', '')}"
        
        self.app.add_api_route(
            path=path,
            endpoint=endpoint_handler,
            methods=[method.upper()],
            name=route["name"]
        )
    
    def _create_response(self, response_data: Dict[str, Any]) -> Response:
        status_code = response_data.get("status_code", 200)
        headers = response_data.get("headers", {})
        body = response_data.get("body", "")
        
        content_type = headers.get("Content-Type", "")
        
        if "application/json" in content_type.lower():
            try:
                json_body = json.loads(body) if isinstance(body, str) else body
                return JSONResponse(content=json_body, status_code=status_code, headers=headers)
            except (json.JSONDecodeError, TypeError):
                pass
        
        return Response(
            content=body,
            status_code=status_code,
            headers=headers,
            media_type=content_type or "text/plain"
        )
    
    def run(self):
        import uvicorn
        print(f"Starting mock server on http://0.0.0.0:{self.port}")
        print(f"Collection ID: {self.collection_id}")
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)