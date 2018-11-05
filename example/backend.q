\l ../jsonrestapi.q

\e 1

user:flip `name`sessionToken!(`Lauren`Kyle`Dan;3#enlist "unset")
event:flip `timestamp`username`description!((2018.11.05T09:21:35.000;2018.11.05T09:21:35.033;2018.11.05T09:21:35.066);(`Kyle`Dan`Lauren);("Started server";"Wrote some tests";"Made the tests pass"))

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

.get.serve["/event/get/:username";
  {[req]
    -1 "Getting events";
    events:select from event where username=`$req[`params;`username];
    .jra.jsonResponse events}]

.post.serve["/event/capture";
  {[req]
    -1 "Capturing event";
    token:.jra.sessionCookie req;
    username:first exec name from user where sessionToken~\:token;
    -1 "From session token, you are identified as " , string username;
    if[any(null username;1<>count username;(-11h)<>type username); :.jra.unauthorizedResponse[]];
    -1 "Identification successful";
    event::event,`timestamp`username`description!(.z.Z;`Kyle;req[`body;`description]);
    .jra.jsonResponse ()}]

.jra.listen 8000
