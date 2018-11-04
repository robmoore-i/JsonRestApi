\l ../jsonrestapi.q

\e 1

user:flip `id`name!(0 1 2;`Lauren`Kyle`Dan)
event:flip `id`description!(0 1 2;("Started server!";"Wrote some tests";"Made the tests pass"))

.post.serve["/identify";
  {[req]
    -1 "Identifying as ",username:req[`body;`username];
    $[(`$username) in user`name;
      .jra.authenticatedJsonResponse[sessionToken:64?0x0;()];
      .jra.unauthorizedResponse[]]}]

.get.serve["/event/get/:eventid";
  .res.ok {[req]
    -1 "Getting event with id ",string eventid:"J"$req[`params;`eventid];
    description:exec description from event where id=eventid;
    (enlist `event)!description}]

.jra.listen 8000
