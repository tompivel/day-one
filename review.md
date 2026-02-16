## Manual review

Alright, now registration works. Please push these changes to the repo. 

Also, the creation of a new plan doesn't work. For example, this request returns a 404 Not Found:
```
curl 'http://localhost:8000/plans/4/' \
  -X POST \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Accept-Encoding: gzip, deflate, br, zstd' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0b21waXZlbCIsImV4cCI6MTc3MTI3MzM5MH0.IdI8wMS4Vy6LwSfoN_0YAwZOyhjMTZoUGT52z4cdzPI' \
  -H 'Origin: http://localhost:5173' \
  -H 'Sec-GPC: 1' \
  -H 'Connection: keep-alive' \
  -H 'Referer: http://localhost:5173/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'Priority: u=0' \
  --data-raw '{"title":"kaskfjaskfj","description":"asfjkasjfkaj"}'
```
The response detail is: {"detail":"Not Found"}. Fix this issue.
