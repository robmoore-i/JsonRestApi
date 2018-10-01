# JSON REST API

Here is a description of a very common piece of functionality.

1. Query endpoint "/get/data" on the backend
2. Backend reads a database
3. Backend responds with some JSON

This code aims to make this as easy as it should be in every language.
After brief google searches I find this kind of simplicity present only in
Kotlin(Http4k) and NodeJS(Express).

## Example Usage

This is designed to be used in a file-at-a-time manner. One file denotes one q
process, which listens on one port. Here is an example of such a file, "backend.q".
This file can be found in the example/ directory of this repository.

```
// backend.q
\l jsonrestapi.q

.get.serve["/";
  {[req]
    raze "Hello there, my favourite browser:  ", raze req[`headers;`$"User-Agent"]}]

.get.serve["/hello";
  {[req]
    "hello"}]

.get.serve["/json";
  {[req]
    `a`b`c!1 2 3}]

.post.serve["/goodbye";
  {[req]
    raze "Goodbye now ",raze req[`body;`name]}]

.jra.listen 8000
```

This file is easy to test in postman. (Note: To send JSON in postman, use the "raw" option in the "body" tab of your request).

## Structures

I construct slightly nicer structures from the interface provided automatically by .z.ph and .z.pp.

Endpoint functions take in a request of the appropriate method, and should return any q structure.
This structure will be serialized into JSON and returned to the sender.

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
    "Postman-Token": "dfe19989-9242-646c-58a6-c2ea8babe8e2",
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
    "Postman-Token": "bb886b62-95b3-5903-9693-b7c5b9ffb825",
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

## Caveats

1. There is no authentication. If you want that, you'll need something slightly more heavyweight.
2. Only supports GET and POST methods.
3. Probably buggy as fuck, I hacked it out tonight after work because I needed it for something else.
