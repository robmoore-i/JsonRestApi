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
This file can be found in the test/ directory of this repository.

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
    "pathargs -> " , req[`pathparams;`a] , " -> " , req[`pathparams;`b]}]

.jra.listen 8000
```

See test.py within the test/ directory for the behaviour of this server. in
order to run the tests, you will need to have the QHOME environment variable set.
For running the tests you'll also need a couple of python libraries (requests, assertpy).

## Structures

I construct nicer structures from the interface provided automatically by `.z.ph` and `.z.pp`.

Endpoint functions take in a request of the appropriate method (either GET or POST), and return a valid HTTP response as a list of string lines. There are a couple of functions in the `.jra` namespace for creating HTTP responses out of any Q structure with `content-type: json`.

1. `.jra.jsonResponse`

This takes a Q object and returns a valid HTTP response by serializing its argument into json using `.j.j`.

2. `.jra.authenticatedJsonResponse`

Does the same as `.jra.jsonResponse`, but also takes a session token as an argument and adds a `Set-Cookie` header containing a cookie called `sid` whose value is this session token.

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

To do cross-origin resource sharing (CORS), your server must verify that any resources provided by it are intended for the recipient in question. To do this, an Access-Control-Allow-Origin header is required. In the same directory as your `backend.q` you can create a file called `config.q` which contains a value `.config.frontendOrigin`. This is a string of the origin of the recipient your server is intended to serve. If no config is provided, the value defaults to "*", which means that its resources are safe to use by any origin.

## Caveats

- Only supports GET and POST methods.
- Path parameters are only supported for GET requests (POST data should go in the body).
