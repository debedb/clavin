# Postman Mock Server

A Python clone of Postman's mock server functionality using FastAPI.

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

Start the mock server with a Postman collection ID:

```bash
python3 main.py YOUR_COLLECTION_ID
```

Or specify a custom port:

```bash
python3 main.py YOUR_COLLECTION_ID --port 8080
```

The server will:
1. Fetch the collection from Postman API
2. Parse all requests and their examples
3. Start a FastAPI server on localhost
4. Serve mock responses based on the first example for each request

## Features

- ✅ Fetches collections from Postman API
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