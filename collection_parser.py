from typing import Dict, List, Any, Optional
import json
import re


class CollectionParser:
    def __init__(self, collection_data: Dict[str, Any]):
        self.collection = collection_data["collection"]
        self.routes = []
    
    def parse(self) -> List[Dict[str, Any]]:
        self._parse_items(self.collection.get("item", []))
        return self.routes
    
    def _parse_items(self, items: List[Dict[str, Any]], base_path: str = ""):
        for item in items:
            if "item" in item:
                folder_path = base_path + "/" + item.get("name", "")
                self._parse_items(item["item"], folder_path)
            else:
                self._parse_request(item, base_path)
    
    def _parse_request(self, item: Dict[str, Any], base_path: str):
        request = item.get("request", {})
        if not request:
            return
        
        method = request.get("method", "GET").upper()
        url_obj = request.get("url", {})
        
        if isinstance(url_obj, str):
            path = self._extract_path_from_url(url_obj)
        else:
            path = self._build_path_from_url_obj(url_obj)
        
        if not path:
            return
        
        example = self._get_first_example(item)
        if not example:
            example = self._create_default_response()
        
        route = {
            "method": method,
            "path": path,
            "name": item.get("name", "Unknown"),
            "response": example
        }
        
        self.routes.append(route)
    
    def _extract_path_from_url(self, url: str) -> str:
        if "{{" in url:
            url = re.sub(r'\{\{[^}]+\}\}', 'localhost:8000', url)
        
        if url.startswith("http"):
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.path
        return url if url.startswith("/") else "/" + url
    
    def _build_path_from_url_obj(self, url_obj: Dict[str, Any]) -> str:
        raw = url_obj.get("raw", "")
        if raw:
            return self._extract_path_from_url(raw)
        
        path_parts = url_obj.get("path", [])
        if path_parts:
            path = "/" + "/".join(str(part) for part in path_parts)
            return path.replace("{{", "{").replace("}}", "}")
        
        return "/"
    
    def _get_first_example(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        response_examples = item.get("response", [])
        if response_examples:
            first_example = response_examples[0]
            return {
                "status_code": first_example.get("code", 200),
                "headers": self._parse_headers(first_example.get("header", [])),
                "body": first_example.get("body", "")
            }
        return None
    
    def _parse_headers(self, headers: List[Dict[str, Any]]) -> Dict[str, str]:
        header_dict = {}
        for header in headers:
            key = header.get("key", "")
            value = header.get("value", "")
            if key and value:
                header_dict[key] = value
        return header_dict
    
    def _create_default_response(self) -> Dict[str, Any]:
        return {
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": '{"message": "Mock response"}'
        }