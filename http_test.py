import http

message = 'POST /foo HTTP/1.1\r\nContent-Type: application/json\r\nContent-Length: 4\r\n\r\n{"hello": "world"}\r\n'
request = http.parse(message)

assert request.method == "POST", "parses request method correctly"
assert request.path == "/foo", "parses request path correctly"

assert len(request.headers) == 2, "parses request headers correctly"
assert request.headers[0].name == "Content-Type", "parses request headers correctly"
assert (
    request.headers[0].value == "application/json"
), "parses request headers correctly"
assert request.headers[1].name == "Content-Length", "parses request headers correctly"
assert request.headers[1].value == "4", "parses request headers correctly"

# TODO(christianscott): is this correct?
assert request.body == '\n{"hello": "world"}\n', "parses request body correctly"

print("all tests passed")
