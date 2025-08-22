#!/usr/bin/env python3

import click
import sys
from typing import Tuple, List, Optional
from mock_server import MockServer


class CollectionSpec:
    """Handles parsing of collection specifications with optional roots."""
    
    def __init__(self):
        self.collections = []
    
    def add(self, spec: str):
        """Add a collection spec in format 'ID' or 'ID:root'."""
        if ':' in spec:
            collection_id, root = spec.split(':', 1)
            if not root.startswith('/'):
                raise ValueError(f"Root path must start with '/': {root}")
            self.collections.append((collection_id, root))
        else:
            self.collections.append((spec, None))
    
    def get_collections(self):
        return self.collections


@click.command()
@click.option('--collection', '-c', 'collection_specs', multiple=True,
              help='Collection ID with optional root path. Can be specified multiple times. '
                   'Format: --collection <ID> or --collection <ID>:/root '
                   'Example: --collection abc123 --collection def456:/api/v2')
@click.option('--port', '-p', type=int, help='Port to run the mock server on (random if not specified)')
def main(collection_specs: Tuple[str, ...], port: int):
    """
    Start a Postman mock server for one or more collections.
    
    Examples:
        # Single collection
        clavin --collection <ID>
        
        # Multiple collections with automatic conflict detection
        clavin --collection <ID1> --collection <ID2>
        
        # Multiple collections with root paths to avoid conflicts
        clavin --collection <ID1>:/api/v1 --collection <ID2>:/api/v2
    """
    if not collection_specs:
        click.echo("Error: At least one collection must be specified", err=True)
        sys.exit(1)
    
    try:
        # Parse collection specifications
        parser = CollectionSpec()
        for spec in collection_specs:
            parser.add(spec)
        
        collections = parser.get_collections()
        
        server = MockServer(collections, port)
        server.setup_routes()
        server.run()
    except ValueError as e:
        click.echo(f"Configuration error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()