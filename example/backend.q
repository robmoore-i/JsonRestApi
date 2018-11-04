\l ../jsonrestapi.q

user:flip `id`name!(0 1 2;`Lauren`Kyle`Dan)

.post.serve["/identify";
  {[req]
    .jra.authenticatedJsonResponse[sessionToken:64?0x0;()]
  }]

.jra.listen 8000
