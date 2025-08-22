from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import json
import socket
from typing import Dict, List, Any, Tuple, Optional
from postman_client import PostmanClient
from collection_parser import CollectionParser


class MockServer:
    def __init__(self, collections: List[Tuple[str, Optional[str]]], port: int = None):
        """Initialize mock server with multiple collections.
        
        Args:
            collections: List of tuples (collection_id, root_path or None)
            port: Port to run on (random if not specified)
        """
        self.collections = collections
        self.port = port or self._get_free_port()
        self.app = FastAPI(title="Postman Mock Server", version="1.0.0")
        self.routes = []
        self.path_to_collection = {}  # Track which collection owns each path
        
    def _get_free_port(self) -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    def setup_routes(self):
        """Setup routes from all collections with conflict detection."""
        client = PostmanClient()
        all_routes = []
        collection_info = {}  # Store collection names for display
        
        # First, collect all routes from all collections
        for collection_id, root_path in self.collections:
            try:
                collection_data = client.get_collection(collection_id)
                collection_name = collection_data.get('collection', {}).get('info', {}).get('name', 'Unknown Collection')
                collection_info[collection_id] = {'name': collection_name, 'root_path': root_path}
                
                parser = CollectionParser(collection_data)
                routes = parser.parse()
                
                # Apply root path if specified
                if root_path:
                    for route in routes:
                        original_path = route['path']
                        route['path'] = root_path.rstrip('/') + '/' + original_path.lstrip('/')
                        route['collection_id'] = collection_id
                        route['root_path'] = root_path
                else:
                    for route in routes:
                        route['collection_id'] = collection_id
                        route['root_path'] = None
                
                all_routes.extend(routes)
                print(f"Loaded {len(routes)} routes from '{collection_name}' ({collection_id})")
                if root_path:
                    print(f"  Applied root path: {root_path}")
                    
            except Exception as e:
                raise Exception(f"Failed to setup routes from collection {collection_id}: {e}")
        
        # Check for conflicts (same method + path)
        seen_endpoints = {}
        conflicts = []
        
        for route in all_routes:
            endpoint_key = f"{route['method'].upper()} {route['path']}"
            
            if endpoint_key in seen_endpoints:
                existing = seen_endpoints[endpoint_key]
                # Only error if both don't have root paths (explicit roots mean user intended separation)
                if existing['root_path'] is None and route['root_path'] is None:
                    conflicts.append({
                        'endpoint': endpoint_key,
                        'collection1': existing['collection_id'],
                        'collection2': route['collection_id']
                    })
            else:
                seen_endpoints[endpoint_key] = route
        
        if conflicts:
            error_msg = "Path conflicts detected between collections without root paths:\n"
            for conflict in conflicts:
                error_msg += f"  {conflict['endpoint']}: {conflict['collection1']} vs {conflict['collection2']}\n"
            error_msg += "\nPlease specify root paths using --collection <ID> /root syntax to resolve conflicts."
            raise ValueError(error_msg)
        
        # Add all routes
        self.routes = all_routes
        self.collection_info = collection_info  # Store for later use
        for route in self.routes:
            self._add_route(route)
        
        print(f"\nMock server setup complete with {len(self.routes)} total routes:")
        for collection_id, root_path in self.collections:
            collection_routes = [r for r in self.routes if r['collection_id'] == collection_id]
            collection_name = collection_info[collection_id]['name']
            print(f"\nCollection: '{collection_name}'")
            print(f"  ID: {collection_id}")
            print(f"  Routes: {len(collection_routes)}")
            if root_path:
                print(f"  Root path: {root_path}")
            for route in collection_routes[:5]:  # Show first 5 routes
                print(f"    {route['method']} {route['path']} - {route['name']}")
            if len(collection_routes) > 5:
                print(f"    ... and {len(collection_routes) - 5} more")
    
    def _add_route(self, route: Dict[str, Any]):
        method = route["method"].lower()
        path = route["path"]
        response_data = route["response"]
        
        async def endpoint_handler(request: Request):
            # Log incoming request
            print(f"\n>>> INCOMING REQUEST <<<")
            print(f"Method: {request.method}")
            print(f"Path: {request.url.path}")
            print(f"Headers:")
            for name, value in request.headers.items():
                print(f"  {name}: {value}")
            
            response = self._create_response(response_data)
            
            # Log outgoing response
            print(f"\n>>> OUTGOING RESPONSE <<<")
            print(f"Status: {response.status_code}")
            print(f"Headers:")
            for name, value in response.headers.items():
                print(f"  {name}: {value}")
            print()
            
            return response
        
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
        
        # Remove headers that FastAPI handles automatically or that can cause issues
        headers = {k: v for k, v in headers.items() if k.lower() not in ["content-length", "content-encoding"]}
        
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
        print(f"\n{'='*60}")
        print(f"Starting mock server on http://0.0.0.0:{self.port}")
        print(f"{'='*60}")
        print(f"\nServing {len(self.collections)} collection(s):")
        
        for collection_id, root_path in self.collections:
            if hasattr(self, 'collection_info') and collection_id in self.collection_info:
                collection_name = self.collection_info[collection_id]['name']
                print(f"\n  Collection: '{collection_name}'")
                print(f"    ID: {collection_id}")
                if root_path:
                    print(f"    Root: {root_path}")
                else:
                    print(f"    Root: / (default)")
            else:
                # Fallback if collection_info not available
                if root_path:
                    print(f"  - {collection_id} at {root_path}")
                else:
                    print(f"  - {collection_id}")
        
        print(f"\n{'='*60}")
        print("Server is ready to receive requests...")
        print(f"{'='*60}\n")
        
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)