\l ../jsonrestapi.q

jr:.jra.jsonResponse
jacr:.jra.authenticatedJsonResponse["maker";]

.get.serve["/";
  {[req]
    jr raze "Hello there, my favourite browser:  ", raze req[`headers;`$"User-Agent"]}]

.get.serve["/hello";
  {[req]
    jr "hello"}]

.get.serve["/json";
  {[req]
    jr `a`b`c!1 2 3}]

.post.serve["/goodbye";
  {[req]
    jr raze "Goodbye now ",raze req[`body;`name]}]

.get.serve["/cookie";
  {[req]
    jacr "Check your cookies!"}]

.jra.listen 8000
