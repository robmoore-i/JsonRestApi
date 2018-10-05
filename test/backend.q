\l ../jsonrestapi.q

.get.serve["/";
  {[req]
    raze "Hello there, my favourite browser:  ", raze req[`headers;`$"User-Agent"]}]

.get.serve["/hello";
  {[req]
    "hello"}]

.get.serve["/json";
  {[req]
    `a`b`c!1 2 3}]

.post.serve["/goodbye";
  {[req]
    raze "Goodbye now ",raze req[`body;`name]}]

.jra.listen 8000
