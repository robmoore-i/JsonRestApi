\l ../jsonrestapi.q

user:flip `name`sessionToken!(`Lauren`Kyle`Dan;3#enlist "unset")
event:flip `timestamp`username`description`sessionToken!((2018.11.05T09:21:35.000;2018.11.05T09:21:35.033;2018.11.05T09:21:35.066);(`Kyle`Dan`Lauren);("Started server";"Wrote some tests";"Made the tests pass");("kyle-token";"dan-token";"lauren-token"))

// Generates a random session token - 64 random bytes.
generateSessionToken:{raze string 64?0x0}

// Saves a (sessionToken) as the latest valid token under the given (username)
k)beginNewUserSession:{[username;sessionToken]![`user;,(=;`name;,username);0b;(,`sessionToken)!,(enlist;sessionToken)];}

.post.serve["/identify";
  {[req]
    username:`$req[`body;`username];
    if[not username in user`name; :.jra.unauthorizedResponse[]];
    sessionToken:generateSessionToken[];
    beginNewUserSession[username;sessionToken];
    .jra.authenticatedJsonResponse[sessionToken;()]}]

// Returns the name of the user currently in a session using the given (sessionToken)
k)matchUserInSession:{[sessionToken]*:?[`user;,((\:;~);`sessionToken;sessionToken);();`name]}

// Returns true if the given argument is a valid username for the `user table.
isValidUsername:{not any(null x;1<>count x;(-11h)<>type x)}

.post.serve["/event/capture";
  {[req]
    sessionToken:.jra.sessionCookie req;
    username:matchUserInSession sessionToken;
    if[not isValidUsername username; :.jra.unauthorizedResponse[]];
    event::event,`timestamp`username`description`sessionToken!(.z.Z;username;req[`body;`description];sessionToken);
    .jra.jsonResponse ()}]

// Return a table of all events associated with the given (username)
k)getUserEvents:{[username]?[`event;,(=;`username;,username);0b;()]}

.get.serve["/event/get/:username";
  {[req]
    username:`$req[`params;`username];
    events:getUserEvents username;
    .jra.jsonResponse events}]

.jra.listen 8000
