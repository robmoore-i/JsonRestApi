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

// CORS headers
corsAllowOrigin:"Access-Control-Allow-Origin: ",.config.frontendOrigin
corsAllowMethods:{"Access-Control-Allow-Methods: ",x}
corsAllowHeaders:{"Access-Control-Allow-Headers: ",x}
corsHeaders:{[methods;headers]
  corsAllowOrigin,"\r\n",corsAllowMethods[methods],"\r\n",corsAllowHeaders[headers]}

// HTTP OPTIONS generic preflight response: "The frontend can do whatever it wants."
// See: https://stackoverflow.com/questions/10636611/how-does-access-control-allow-origin-header-work
preflightResponse:{[methods;headers]
  okHeader,"\r\n",corsHeaders[methods;headers],"\r\n\r\n"}

// The header for a JSON resposne
jsonHeader:"Content- Type:application/json"

// The header for sending an authentication cookie
setAuthCookieHeader:{"Set-Cookie: sid=",x}

// Create a JSON response from a Q object
jsonResponse:{okHeader,"\r\n",jsonHeader,"\r\n\r\n",.j.j x}

// Create a JSON response from a Q object including a cookie
authenticatedJsonResponse:{okHeader,"\r\n",jsonHeader,"\r\n",setAuthCookieHeader[x],"\r\n\r\n",.j.j y}

// Start listening using the current endpoints on the given port
listen:{[p]
  .z.ph::{
    getreq::.get.request x;
    f:.get.endpoints["/",last "/" vs getreq.url];
    getres::$[ null f ; jsonResponse "none" ; f getreq ];
    getres};
  .z.pp::{
    postreq::.post.request x;
    f:.post.endpoints["/",last "/" vs postreq.url];
    postres::$[ null f ; jsonResponse "none" ; f postreq ];
    postres};
  .z.pm::{
    optreq::`path`headers!(x 1;x 2);
    method:optreq[`headers;`$"access-control-request-method"];
    headers:optreq[`headers;`$"access-control-request-headers"];
    optres::preflightResponse[method;headers];
    optres};
  system "p ",string p;}

////// RESPONSE

\d .res

ok:{[f]
  {[f;req]
    .jra.jsonResponse f req}[f;]}

okWithAuthCookie:{[sid;f]
  {[sid;f;req]
    .jra.authenticatedJsonResponse[sid;f req]}[sid;f;]}
