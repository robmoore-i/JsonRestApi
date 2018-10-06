\l config.q

////// ALL REQUESTS

\d .jra

// Append a new endpoint to the existing dictionary
addEndpoint:{[curEndpoints;path;f]
  path:$[1=count path;enlist path;path];
  curEndpoints , (enlist path)!enlist f}

////// GET REQUESTS

\d .get

// Create a GET request dictionary from the dictionary passed to .z.ph
request:{`url`headers!(((x[1]`Host),"/",x 0);x 1)}

// At the start, there are no assigned GET endpoints
endpoints:()!()

// Associate a GET endpoint with a function
serve:{[path;f]endpoints,: .jra.addEndpoint[endpoints;path;f];}

////// POST REQUESTS

\d .post

// Create a POST request dictionary from the dictionary passed to .z.pp
request:{s:" " vs x 0;`url`headers`body!(((x[1]`Host),"/",s 0);x 1;.j.k raze 1_s)}

// At the start, there are no assigned POST endpoints
endpoints:()!()

// Associate a POST endpoint with a function
serve:{[path;f]endpoints,: .jra.addEndpoint[endpoints;path;f];}

////// General

\d .jra

// HTTP 200 OK
okHeader:"HTTP/1.x 200 OK"

// The header for allowing responses to the server
corsHeader:"Access-Control-Allow-Origin: ",.config.frontendOrigin

// The header for a JSON resposne
jsonHeader:"Content- Type:application/json"

// The header for sending an authentication cookie
setAuthCookieHeader:{"Set-Cookie: sid=",x}

// Create a JSON response from a Q object
jsonResponse:{okHeader,"\r\n",jsonHeader,"\r\n",corsHeader,"\r\n\r\n",.j.j x}

// Create a JSON response from a Q object including a cookie
authenticatedJsonResponse:{okHeader,"\r\n",jsonHeader,"\r\n",setAuthCookieHeader[x],"\r\n\r\n",.j.j y}

// HTTP CORS OPTIONS
corsAllowOrigin:"Access-Control-Allow-Origin: ",.config.frontendOrigin
corsAllowMethods:"Access-Control-Allow-Methods: GET, POST"
corsAllowHeaders:"Access-Control-Allow-Headers: Content-Type"
optionsResponse:okHeader,"\r\n",corsAllowOrigin,"\r\n",corsAllowMethods,"\r\n",corsAllowHeaders,"\r\n\r\n"

// Start listening using the current endpoints on the given port
listen:{[p]
  .z.ph::{
    getreq::.get.request x;
    f:.get.endpoints["/",last "/" vs getreq.url];
    $[ null f ; jsonResponse "none" ; f getreq ]};
  .z.pp::{
    postreq::.post.request x;
    f:.post.endpoints["/",last "/" vs postreq.url];
    $[ null f ; jsonResponse "none" ; f postreq ]};
  .z.pm::{
    optreq::x;
    optionsResponse};
  system "p ",string p;}

////// RESPONSE

\d .res

ok:{[f]
  {[f;req]
    .jra.jsonResponse f req}[f;]}

okWithAuthCookie:{[sid;f]
  {[sid;f;req]
    .jra.authenticatedJsonResponse[sid;f req]}[sid;f;]}
