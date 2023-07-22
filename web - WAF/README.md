# web - WAF
Since the regex pattern is `ecsc23{\\w+}` we can simply set bytes range to remove known part of the flag:
```
curl "https://waf.ecsc23.hack.cert.pl/flag" -H "range: bytes=1-45"
```