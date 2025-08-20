#!/usr/bin/env python3

import click
import sys
from mock_server import MockServer


@click.command()
@click.argument('collection_id')
@click.option('--port', '-p', type=int, help='Port to run the mock server on (random if not specified)')
def main(collection_id: str, port: int):
    """
    Start a Postman mock server for the given collection ID.
    
    COLLECTION_ID: The Postman collection ID to mock
    """
    try:
        server = MockServer(collection_id, port)
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