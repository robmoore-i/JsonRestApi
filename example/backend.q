\l ../jsonrestapi.q

\e 1

user:flip `name`sessionToken!(`Lauren`Kyle`Dan;3#enlist "unset")
event:flip `id`description!(0 1 2;("Started server!";"Wrote some tests";"Made the tests pass"))

.post.serve["/identify";
  {[req]
    -1 "Identifying as ",string username:`$req[`body;`username];
    if[not username in user`name; :.jra.unauthorizedResponse[]];
    sessionToken:raze string 64?0x0;
    ![`user;enlist(=;`name;enlist`Lauren);0b;(enlist`sessionToken)!enlist(enlist;sessionToken)];
    -1 .Q.s user;
    .jra.authenticatedJsonResponse[sessionToken;()]}]

.get.serve["/event/get/:eventid";
  {[req]
    token:.jra.sessionCookie req;
    username:first exec name from user where sessionToken~\:token;
    -1 "From session token, you are identified as " , string username;
    if[any(null username;1<>count username;(-11h)<>type username); :.jra.unauthorizedResponse[]];
    -1 "Getting event with id ",string eventid:"J"$req[`params;`eventid];
    description:exec description from event where id=eventid;
    .jra.jsonResponse (enlist `event)!description}]

.jra.listen 8000
