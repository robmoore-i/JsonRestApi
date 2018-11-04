# Providing RESTful JSON APIs in Q

0. Introduction
1. Background - What is the value in json rest apis?
2. Motivation - Why would we use Q for providing a json rest api?
3. Implementation
4. Demonstration of a real world use-case: Web analytics
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

The code I've produced presents the following API.

```
.get.serve[endpoint;func]  // endpoint is a URL path, func is a unary function taking a HTTP request and returning a HTTP response.
.post.serve[endpoint;func]
.jra.listen[portnumber]
```

Endpoints for get requests can be parameterised, for example "/user/:userid/settings" will match "/user/123/settings" and also "/user/rob/settings". The matched parameter is available for the corresponding function as a value of the request passed to it as an argument. For example:

```
.get.serve["/user/:userid/:propertyname";
  {[req]
    -1 "Getting property {" , req[`params;`propertyname] , "} from user {" , req[`params;`userid] , "}"
    // etc.
  }]
```

Post request endpoints can contain a json message body. This is parsed and made available to the endpoint's corresponding function, again in the request. For example:

```
.post.serve["/save/settings";
  {[req]
    -1 "Saving settings " , raze .Q.s req[`body;`settings]
  }]
```

Once all of the API endpoints have been defined, all that's left is to tell the process to listen on a specific port. For example:

```
.jra.listen 8000
```

### Details

This is the technical part of this blog post, where I'll talk in more detail about the design of the program and some of the interesting pieces of code.

## Demonstration of a real world use-case: Web analytics

For a demonstration, we'll write a simple server for capturing webpage analytics. It is valueable for a business to be able to monitor how users are using their webpages. For this reason, a server for capturing real time web analytics is an important piece of software to have for evolving a widely used frontend. Web analytics is, fundementally, a tick data capture service, which is why I've chosen to use it for this example.

Below is a quick outline of the simple functionality our server will support. It needs to identify users and capture events that take place in the webpage. Our UI/UX engineers will also surely need to use our captured analytics, so we'll need to support an API for serving the stored data as well.

```
// Identifies a user by username and gives them a cookie to track their actions within the context of their current session.
Route: /identify
Method: POST
POST Body: Json of the form {username: `username`}
Function: Checks if the given username is stored on the server and if it is, returns a session token.
Note: I have omitted the use of a password for this endpoint specifically to avoid conveying any illusion of security over plain HTTP.

// Lets our UI/UX engineers access the data
Route: /events/get/:username
Method: GET
Function: Return all of the events captured within sessions of the user with the given username.

// Our frontend posts data back to us about events
Route: /events/capture
Method: POST
Cookie: Requires valid session token
POST Body: JSON: {eventName: `event name`}
Function: Store the data associated with the event recorded by the web page.
```

## Future work

HTTPS

Cookie Authentication (ACTUALLY JUST DO THIS BEFOREHAND)

Asynchronous execution

## References
