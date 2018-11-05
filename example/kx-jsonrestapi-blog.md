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
    // etc.
  }]
```

Once all of the API endpoints have been defined, all that's left is to tell the process to listen on a specific port. For example:

```
.jra.listen 8000
```

## Demonstration of a real world use-case: Web analytics

For a demonstration, we'll write a simple server for capturing webpage analytics. It is valueable for a business to be able to monitor how users are using their webpages. For this reason, a server for capturing real time web analytics is an important piece of software to have for evolving a widely used frontend. Web analytics is, fundementally, a tick data capture service, which is why I've chosen to use it for this example.

### Requirements

Below is a quick outline of the simple functionality our server will support. It needs to identify users and capture events that take place in the webpage. Our UI/UX engineers will also surely need to use our captured analytics, so we'll need to support an API for serving the stored data as well.

```
// Identifies a user by username and gives them a cookie to track their actions within the context of their current session.
Route: /identify
Method: POST
POST Body: Json of the form {username: `username`}
Function: Checks if the given username is stored on the server and if it is, returns a session token.
Note: I have omitted the use of a password for this endpoint specifically to avoid conveying any illusion of robust security over plain HTTP.

// Our frontend posts data back to us about events associated with a given user
Route: /events/capture
Method: POST
Cookie: Requires valid session token
POST Body: JSON: {eventName: `event name`}
Function: Store the data associated with the event recorded by the web page.

// Lets our UI/UX engineers access the data
Route: /events/get/:username
Method: GET
Function: Return all of the events captured within sessions of the user with the given username.
```

### Code

#### The /identify endpoint

When tracking user interactions, we want our data to be tied to a session. To do this, we will give users a session token for us to store with recorded events. To identify with the tracking server and get our web analytics session token, we will post our username, and receive a session token cookie in the response.

Our user table looks like this:

```
user:flip `name`sessionToken!(`Lauren`Kyle`Dan;3#enlist "a-session-token")
```

We'll use 64 random bytes as our session tokens for simplicity.

```
generateSessionToken:{raze string 64?0x0}
```

We also need to be able to set the current session for a given user.

```
k)beginNewUserSession:{[username;sessionToken]![`user;,(=;`name;,username);0b;(,`sessionToken)!,(enlist;sessionToken)];}
```

The endpoint looks like this:

```
.post.serve["/identify";
  {[req]
    username:`$req[`body;`username];                             // Extract the provided username from the POST request body
    if[not username in user`name; :.jra.unauthorizedResponse[]]; // If the username doesn't match one of our users then something went wrong
    sessionToken:generateSessionToken[];                         // Create a session token
    beginNewUserSession[`Lauren;sessionToken];                   // Record the session token for the user's new session
    .jra.authenticatedJsonResponse[sessionToken;()]}]            // Return a response with a Set-Cookie header containing the web analytics tracking cookie.
```

#### The /event/capture endpoint

### Testing a json rest api

In order to deliver quality software fast, it is widely accepted that developers must write automated tests. It is very easy to do a manual test using postman, however I'd like to present a way to create simple integration tests using lightweight and commonly available tools.

### Handling preflight requests using HTTP OPTIONS

Web browsers often perform a preflight request to a web server to validate a request for cross origin resource sharing, which is where the browser confirms that the requested resource is intended for the client. If it isn't, then the user may be at risk of becoming a victim of a cross-site scripting (XSS) attack. To handle the preflight request, a web server looking to provide dynamic data to a frontend must implement a HTTP OPTIONS response. In Q, this can be done very easily by using `.z.pm`.

## Future work

HTTPS

Asynchronous execution

## Further reading

### HTTP

.z.ph - HTTP GET
.z.pp - HTTP POST
.z.ac - Authenticate from cookie
.z.pm - HTTP OPTIONS

## JSON

.j.j - Serialize into JSON
.j.k - Deserialize from JSON

## References
