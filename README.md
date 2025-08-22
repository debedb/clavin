# Clavin - Postman Mock Server

A Python clone of Postman's mock server functionality using FastAPI with support for multiple collections.

## Setup

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Create a `.env` file with your Postman API credentials:
```bash
cp .env.example .env
```

Edit the `.env` file and add your Postman API key:
```
POSTMAN_API_KEY=your_postman_api_key_here
POSTMAN_VAULT_KEY=your_postman_vault_key_here
```

## Usage

### Single Collection

Start the mock server with a single Postman collection:

```bash
python3 main.py --collection YOUR_COLLECTION_ID
```

Or specify a custom port:

```bash
python3 main.py --collection YOUR_COLLECTION_ID --port 8080
```

### Multiple Collections

Serve multiple collections simultaneously:

```bash
python3 main.py --collection COLLECTION_ID_1 --collection COLLECTION_ID_2
```

If collections have conflicting endpoints (same method and path), specify root paths to avoid conflicts:

```bash
python3 main.py --collection COLLECTION_ID_1:/api/v1 --collection COLLECTION_ID_2:/api/v2
```

This will serve:
- Collection 1's endpoints under `/api/v1/*`
- Collection 2's endpoints under `/api/v2/*`

The server will:
1. Fetch all specified collections from Postman API
2. Parse all requests and their examples from each collection
3. Detect and report any endpoint conflicts between collections
4. Start a FastAPI server on localhost
5. Serve mock responses based on the first example for each request

## Features

- ✅ Fetches collections from Postman API
- ✅ Supports multiple collections simultaneously
- ✅ Automatic conflict detection between collections
- ✅ Root path specification to avoid endpoint conflicts
- ✅ Parses requests and examples from collections
- ✅ Serves mock responses on localhost
- ✅ Supports custom port or random port selection
- ✅ Uses first example when multiple examples exist
- ✅ Handles JSON and text responses
- ✅ Preserves response headers and status codes

## Getting Your Collection ID

1. Open your collection in Postman
2. Click the "..." menu next to your collection name
3. Select "Share collection"
4. The collection ID is in the URL or can be found in the collection info

## Limitations

- Currently uses the first example when multiple examples exist
- Only runs on localhost
- No environment variable substitution yet
- No authentication support yet

See [TODO.md](TODO.md) for planned enhancements.