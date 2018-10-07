# JSON REST API

Here is a description of a very common piece of functionality.

1. Query endpoint "/get/my/data" on the backend
2. Backend reads a database
3. Backend responds with some JSON

This code aims to make this as easy as it should be in every language.
I have experienced this kind of simplicity only in Kotlin(Http4k) and NodeJS(Express).
The results of my google searches regarding solutions for other languages in which I would
expect this ease and simplicity (Python, J, Haskell) are disappointing.

## Example Usage

This is designed to be used in a file-at-a-time manner. One file denotes one q
process, which listens on one port. Here is an example of such a file, "backend.q".
This file can be found in the example/ directory of this repository.

```
// backend.q

\l ../jsonrestapi.q

.get.serve["/";
  .res.ok {[req]
    raze "Hello there, my favourite browser:  ", raze req[`headers;`$"User-Agent"]}]

.get.serve["/hello";
  .res.ok {[req]
    "hello"}]

.get.serve["/json";
  .res.ok {[req]
    `a`b`c!1 2 3}]

.post.serve["/goodbye";
  .res.ok {[req]
    raze "Goodbye now ",raze req[`body;`name]}]

.get.serve["/cookie";
  .res.okWithAuthCookie["s355IonT0k3n";] {[req]
    "Check your cookies!"}]

.get.serve["/pathargs/:a/:b";
  .res.ok {[req]
    "pathargs -> " , req[`params;`a] , " -> " , req[`params;`b]}]

.jra.listen 8000
```

See test.py within the test/ directory for the behaviour of this server. in
order to run the tests, you will need to have the QHOME environment variable set.
You'll also need a couple of python libraries (requests, assertpy).

## Structures

I construct nicer structures from the interface provided automatically by `.z.ph` and `.z.pp`.

Endpoint functions take in a request of the appropriate method (either GET or POST), and should return any q structure. This structure will be serialized into JSON and returned to the sender. If there you have used parameters encoded in the path of the served endpoint, then these are accessible as an additional key of the request dictionary called 'params'.

The wrappers `.res.ok` and `.res.okWithAuthCookie` wrap the server's functions so that their return value (any q structure) is wrapped with a HTTP header, setting content-type to application/json and serializing the resultant q object into JSON using `.j.j`. This is then sent back to the sender.

### Get request

These are q dictionaries of the following format.

```
{
  "url":" localhost:8000/",
  "headers": {
    "Host": "localhost:8000",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
  }
}
```

### Post request

These are q dictionaries of the following format.

The JSON booleans, true and false, are mapped to q booleans 1b and 0b as appropriate.

```
{
  "url": "localhost:8000/",
  "headers": {
    "Host": "localhost:8000",
    "Connection": "keep-alive",
    "Content-Length": "41",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "Cache-Control": "no-cache",
    "Origin": "chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop",
    "Content-Type": "text/plain;charset=UTF-8",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
  },
  "body": {
    "number": 5,
    "string": "hello",
    "bool": true
  }
}
```

## Config

You need a `config.q` file in the same directory as you call your server from.

For the above example, I have `config.q` in the same directory as `backend.q`.

## Caveats

- Only supports GET and POST methods.
- Path parameters are only supported for GET requests (POST data should go in the body).
