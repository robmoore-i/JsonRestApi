\l ../jsonrestapi.q

\e 1

user:flip `name`sessionToken!(`Lauren`Kyle`Dan;3#enlist "unset")
event:flip `timestamp`username`description!((2018.11.05T09:21:35.000;2018.11.05T09:21:35.033;2018.11.05T09:21:35.066);(`Kyle`Dan`Lauren);("Started server";"Wrote some tests";"Made the tests pass"))

// Generates a random session token - 64 random bytes.
generateSessionToken:{raze string 64?0x0}

// Saves a (sessionToken) as the latest valid token under the given (username)
beginNewUserSession:{[username;sessionToken]![`user;enlist(=;`name;enlist username);0b;(enlist`sessionToken)!enlist(enlist;sessionToken)];}

.post.serve["/identify";
  {[req]
    -1 "Identifying as ",string username:`$req[`body;`username];
    if[not username in user`name; :.jra.unauthorizedResponse[]];
    sessionToken:generateSessionToken[];
    beginNewUserSession[`Lauren;sessionToken];
    -1 .Q.s user;
    .jra.authenticatedJsonResponse[sessionToken;()]}]

// Returns the name of the user currently in a session using the given (sessionToken)
matchUserInSession:{[sessionToken]first ?[`user;enlist((\:;~);`sessionToken;sessionToken);();`name]}

// Returns true if the given argument is a valid username for the `user table.
isValidUsername:{not any(null x;1<>count x;(-11h)<>type x)}

.post.serve["/event/capture";
  {[req]
    -1 "Capturing event";
    sessionToken:.jra.sessionCookie req;
    username:matchUserInSession sessionToken;
    -1 "From session token, you are identified as " , string username;
    if[not isValidUsername username; :.jra.unauthorizedResponse[]];
    -1 "Identification successful";
    event::event,`timestamp`username`description!(.z.Z;username;req[`body;`description]);
    .jra.jsonResponse ()}]

// Return a table of all events associated with the given (username)
getUserEvents:{[username]?[`event;enlist(=;`username;enlist username);0b;()]}

.get.serve["/event/get/:username";
  {[req]
    -1 "Getting events";
    username:`$req[`params;`username];
    events:getUserEvents username;
    .jra.jsonResponse events}]

.jra.listen 8000
