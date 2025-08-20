# TODO: Postman Mock Server Enhancements

## Multiple Examples Support
- [ ] Add functionality to select which example to use when multiple examples exist for a request
- [ ] Add CLI option to specify example selection strategy (first, last, random, by name)
- [ ] Add interactive mode to choose examples during startup

## Environment Variables Support
- [ ] Parse and apply Postman environment variables in requests/responses
- [ ] Support variable substitution in URLs, headers, and response bodies
- [ ] Add support for POSTMAN_VAULT_KEY for accessing private environments

## Advanced Mock Features
- [ ] Add delay simulation for responses
- [ ] Support for conditional responses based on request parameters
- [ ] Add request validation against schema
- [ ] Support for dynamic response generation

## Server Management
- [ ] Add health check endpoint
- [ ] Add endpoint to list all available routes
- [ ] Add endpoint to reload collection without restart
- [ ] Add logging and metrics

## External Domain Support
- [ ] Add support for running on external domains (not just localhost)
- [ ] Add SSL/TLS support
- [ ] Add authentication/authorization middleware

## Error Handling
- [ ] Better error messages for invalid collection IDs
- [ ] Graceful handling of malformed Postman collections
- [ ] Network error retry logic for Postman API calls

## Testing
- [ ] Add unit tests for collection parser
- [ ] Add integration tests for mock server
- [ ] Add CLI tests