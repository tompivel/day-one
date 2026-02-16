## Manual review

Plan, macrocycle and microcycle creation works. Clicking on each of these on the dashboard correctly directs you through the chain (Plan -> Macrocycle -> Microcycle -> Session). However, Session creation doesn't work. It particulary seems a problem with date formatting. The request sent on curl format was:
```
curl 'http://localhost:8000/sessions/1/' \
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
  --data-raw $'{"sport":"Running","date_start":"2026-02-11T03:00:00.000Z","duration_minutes":50,"perceived_exertion":3,"description":"Easy 50\' session for the day\041"}'```

The answer was a 422, with detail:
```
{"detail":[{"type":"date_from_datetime_inexact","loc":["body","date_start"],"msg":"Datetimes provided to dates should have zero time - e.g. be exact dates","input":"2026-02-11T03:00:00.000Z"}]}
```

Please fix this issue.
