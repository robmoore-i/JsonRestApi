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

The code I've produced presents the following API from within a .jra namespace, which stands for "(j)son (r)est (a)pi".

```
.jra.get[endpoint;func] // endpoint is a URL path, func is a unary function taking a HTTP request and returning a HTTP response.
.jra.post[endpoint;func]
.jra.listen[portnumber]
```



## Demonstration of a real world use-case

## Future work

HTTPS

Cookie Authentication

## References
