# Providing RESTful JSON APIs in Q

0. Introduction
1. Background - What is the value in json rest apis?
2. Motivation - Why would we use Q for providing a json rest api?
3. Implementation
4. Demonstration of a real world use-case: Web analytics
5. Future work
6. Helpful links

## Introduction

When I started writing my implementation of a Q json rest api, I was looking for some common functionality:

1. Query endpoint "http://myserver.com/get/my/data" on the backend
2. Backend reads a database
3. Backend responds with JSON containing some records

In this blog post I will discuss how we can use Q to deliver this value extremely quickly.

## Background - What is the value in json rest apis?

JSON is a lightweight, text-based format for storing data. It stands for "(J)ava(S)cript (O)bject (N)otation". The primary domain of JSON is as a format for transferring data from a server (backend rest api) to a client (javascript frontend). Within this problem-space, JSON competes with formats like XML, however, JSON has a combination of favourable properties:

1. JSON can be parsed as a Javascript object
2. JSON is lightweight
3. JSON is more human readable

We want our frontends to be responsive. It makes sense then, that we would favour a data-format which parses straight into Javascript. An additional benefit is that for simple data, its non-verbosity in comparison to alternatives makes it relatively efficient to communicate over the network.

Having a more human readable format helps the development team design and deliver their API faster than they would otherwise, an advantage that is worth noting even though "human readable-ness" is not a property that has many hard metrics associated with it.

## Motivation - Why would we use Q for providing a json rest api?

Q is an intuitive choice to provide this behaviour, because it supports persistence, JSON parsing and HTTP request handling, out-of-the-box and within an already very expressive programming language. By using a lightweight Q implementation, we can write less code, which will enable us to adapt our backend to changing requirements faster and deliver value faster.

## Implementation

Q provides built in solutions for both handling HTTP requests and making database accesses. Our aim is to model the server as a function. These functions can be thought of as having the signiture `Endpoint -> Request -> Response` - that is, they map and endpoint to a function which recieves a request and returns a response.

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

For a demonstration, we'll pretend we're writing a server for capturing webpage analytics, that is, how users are interacting with a firm's webpages. Web analytics is, fundementally, a tick data capture service, which is why I've chosen to use it for this example. Even though it's not real, this example serves to demonstrate the real value of being able to rapidly create json rest apis in Q, as well as showing the major features of this piece of code I wrote.

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
    beginNewUserSession[username;sessionToken];                  // Record the session token for the user's new session
    .jra.authenticatedJsonResponse[sessionToken;()]}]            // Return a response with a Set-Cookie header containing the web analytics tracking cookie.
```

#### The /event/capture endpoint

The central value proposition in a web analytics platform is capturing user events, so we of course need our json rest api to be able to have events posted to it. To associated captured events with a user session, we'll include the tracking cookie with the request.

Our table of events looks like this:

```
event:flip `timestamp`username`description`sessionToken!((2018.11.05T09:21:35.000;2018.11.05T09:21:35.033;2018.11.05T09:21:35.066);(`Kyle`Dan`Lauren);("Started writing the server";"Wrote a failing test";"Made the test pass");("kyle-token";"dan-token";"lauren-token"))
```

We'll have a constructor to create a new event.

```
newEvent:{[username;description;sessionToken]
  `timestamp`username`description`sessionToken!(.z.Z;username;description;sessionToken)}
```

From the session token supplied by the client we need to get the associated username. If none exists, then we'll inform the sender that their event capture request has an invalid token.

```
matchUserInSession:{[sessionToken]
  username:first ?[`user;enlist((\:;~);`sessionToken;sessionToken);();`name];
  $[all(not null x;1=count x;(-11h)=type x);username;`]}
```

The endpoint looks like this:

```
.post.serve["/event/capture";
  {[req]
    sessionToken:.jra.sessionToken req;                                   // Extract the session token from the request
    username:matchUserInSession sessionToken;                             // Get the username matching the session token
    if[null username; :.jra.unauthorizedResponse[]];                      // If there's no matching username, respond with identification failure message.
    event::event,newEvent[username;req[`body;`description];sessionToken]; // Register the captured event 
    .jra.jsonResponse ()}]
```

#### The /event/get/:username endpoint

We also need to provide an API (however primitive) for accessing the captured data. For the purposes of this demo, getting events by username will do.

We'll have a local function to perform the query on the server:

```
k)getUserEvents:{[username]?[`event;,(=;`username;,username);0b;()]}
```

All the endpoint does it take the username from the request, feed it to the prepared query and regurgitate the results in the response.

```
.get.serve["/event/get/:username";
  {[req]
    username:`$req[`params;`username]; // Extract the username from the request
    events:getUserEvents username;     // Perform the query to get the requested data
    .jra.jsonResponse events}]         // Return the data as JSON in the response
```

#### Starting the server

At the end of our file that specifies our server, we need to finally tell it to use the provided API specification to listen on a port.

```
.jra.listen 8000
```

At this point we can query it as we like. We can have this as a live system, or we might just be starting it up to run some integration tests on it.

### Handling preflight requests using HTTP OPTIONS

Web browsers often perform a preflight request to a web server to validate a request for cross origin resource sharing, which is where the browser confirms that the requested resource is intended for the client. If it isn't, then the user may be at risk of becoming a victim of a cross-site scripting (XSS) attack. To handle the preflight request, a web server looking to provide dynamic data to a frontend must implement a HTTP OPTIONS response. In Q, this can be done very easily by using `.z.pm`.

## Future work

These are topics which are beyond the scope of this article, but would be very likely required in a production system.

#### HTTPS

By setting some environment variables and using the -E command line flag with the appropriate argument, you can enable a Q process to run in TLS server mode, which will cause it to communicate using HTTPS rather than HTTP. I've included a link to the relevant section of the reference in the links section at the end.

#### Asynchronous execution

When requests arrive at the server, the world is stopped for the duration of the construction of the response, including during the query. It is fortunate that Q is so fast, but in general we would much rather implement some kind of job queue with worker threads picking requests off the queue and responding individually to enable concurrent responses. This would also demand the specification of a consistency model for the database, as well as the required specification.

## Helpful links

[.z.ph - HTTP GET](https://code.kx.com/q/ref/dotz/#zph-http-get)

[.z.pp - HTTP POST](https://code.kx.com/q/ref/dotz/#zpp-http-post)

[.z.ac - Authenticate from cookie](https://code.kx.com/q/ref/dotz/#zac-http-auth-from-cookie)

[.z.pm - HTTP OPTIONS](https://code.kx.com/q/ref/dotz/#zpm-http-options)

[.j.j - Serialize into JSON](https://code.kx.com/q/ref/dotj/#jj-serialize)

[.j.k - Deserialize from JSON](https://code.kx.com/q/ref/dotj/#jk-deserialize)

[-E - enable TLS server mode](https://code.kx.com/q/cookbook/ssl/#tls-server-mode)