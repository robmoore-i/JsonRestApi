# Providing RESTful JSON APIs in Q

0. Introduction
1. Background - What is the value in json rest apis?
2. Motivation - Why would we use Q for providing a json rest api?
3. How?
4. Demonstration of a real world use-case
5. Future work: HTTPS
6. References

## Introduction

When I started writing my implementation of a Q json rest api, I was looking for some common functionality:

1. Query endpoint "http://myserver.com/get/my/data" on the backend
2. Backend reads a database
3. Backend responds with JSON containing some records

In this blog post I will discuss how we can use Q to deliver this extremely quickly.

## Background - What is the value in json rest apis?

JSON is a lightweight, text-based format for storing data. It stands for "(J)ava(S)cript (O)bject (N)otation". The primary domain of JSON is as a format for transferring data from a server (backend rest api) to a client (javascript frontend). Within this problem-space, JSON competes with formats like XML and yaml, however, JSON has a combination of favourable properties:

1. JSON can be parsed as a Javascript object
2. JSON is lightweight
3. JSON is human readable

We want our frontends to be responsive. It makes sense then, that we would favour a data-format which parses straight into Javascript. An additional benefit is that for simple data, its non-verbosity in comparison to alternatives makes it relatively efficient to communicate over the network.

Having a human readable format helps the development team design and deliver their API faster than they would otherwise, an advantage that is worth noting even though "human readable-ness" is not a property that has many hard metrics associated with it.

## Motivation - Why would we use Q for providing a json rest api?

Q is an intuitive choice to provide this behaviour, because it supports persistence, JSON parsing and HTTP request handling, out-of-the-box and within an already very expressive programming language. By using a lightweight Q implementation, we can write less code, which will enable us to adapt our backend to changing requirements faster and deliver value faster.

## Implementation

Q provides built in solutions for both handling HTTP requests and making database accesses. Our aim is to model the server as a function. These functions have the signiture `Endpoint -> Request -> Response`.

### Usage

The code I've produced presents the following API from within the .jra namespace, which stands for "(j)son (r)est (a)pi".

```
.jra.get[endpoint;func] // endpoint is a URL path, func is a unary function taking a HTTP request and returning a HTTP response.
.jra.post[endpoint;func]
.jra.listen[portnumber]
```

Endpoints for get requests can be parameterised, for example "/user/:userid/settings" will match "/user/123/settings" and also "/user/rob/settings". The matched parameter is available for the corresponding function as a value of the request passed to it as
an argument. For example:

```
```

Post request endpoints can contain a json message body. This is parsed and made available to the endpoint's corresponding function, again in the request. For example:

```
```

Once all of the API endpoints have been defined, all that's left is to tell the process to listen on a specific port. For example:

```
```

### Details

This is the technical part of this blog post, where I'll talk in more detail about the design of the program and some of the interesting pieces of code. 

## Demonstration of a real world use-case

I am building an app. I want to persist some dynamic data onto a server and then provide an API to access and manipulate it. Note that I could be talking about literally almost any of the various apps you have used today.

On the frontend we will have an interface for interacting with the server which is (hopefully...) decoupled from our application logic. Let's say it uses the very straightforward and popular fetch library. I've omitted some trivial implementation details, because all that's important here is the interface.

```
// Server.js
// Contains the prototype for server objects.

export function Server() {
    return {
        sessionToken: null,
        setSessionToken = ((sessionToken) => {this.sessionToken = sessionToken}).bind(this) // Bind `this` to current context
        
        let fetchGET  = (endpoint)       => fetch(...) // Implementation omitted, sends sessionToken as cookie
        let fetchPOST = (endpoint, data) => fetch(...) // Implementation omitted, sends sessionToken as cookie
        
        authenticate: async (username, passwordDigest) => {
            let payload = {username: username, passwordDigest: passwordDigest}
            return fetchGET("authenticate", JSON.stringify(payload))
                .then(response => {
                    let cookie = ...       // Implementation omitted, uses response
                    let sessionToken = ... // Implementation omitted, uses cookie
                    setSessionToken(sessionToken)
                })
        },

        fetchMyData: (dataID) => {
            return fetchGET("getdata/" + String(dataID))
        },

        saveMyData: (dataID, hexBytes) => {
            let payload = {dataid: dataID, hex: hexBytes}
            return fetchPOST("postdata"), JSON.stringify(payload))
        }
    }
}

export const server = Server()
```

Our backend then, must provide these two endpoints and their associated behaviour. Here's a rough specification we might create to fulfil this purpose:

```
Route: /authenticate
Method: POST
POST Body: Json of the form {username: `username`, passwordDigest: `password-digest`}
Function: Checks if username stored on the server has a password which matches the provided digest.
Note: You should not send passwords in plaintext ever, but it would be especially careless to do this without HTTPS.

Route: /getdata/:dataid
Method: GET
Function: Return the bytes stored under the key {dataid} as a hex string
Requires session token

Route: /postdata
Method: POST
POST Body: Json of the form {dataid: `key to store data under`, hex: `string of hex bytes to store`}
Function: Persistently stores the hex bytes using the dataid provided as the key.
Requires session token

```

## Future work

HTTPS

Cookie Authentication (ACTUALLY JUST DO THIS BEFOREHAND)

Asynchronous execution

## References
