\l ../jsonrestapi.q

ok:.res.ok
okWithAuthCookie:.res.okWithAuthCookie

.get.serve["/";
  ok {[req]
    raze "Hello there, my favourite browser:  ", raze req[`headers;`$"User-Agent"]}]

.get.serve["/hello";
  ok {[req]
    "hello"}]

.get.serve["/json";
  ok {[req]
    `a`b`c!1 2 3}]

.post.serve["/goodbye";
  ok {[req]
    raze "Goodbye now ",raze req[`body;`name]}]

.get.serve["/cookie";
  okWithAuthCookie["s355IonT0k3n";] {[req]
    "Check your cookies!"}]

.jra.listen 8000
