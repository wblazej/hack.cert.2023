# [crypto - Mind Blank](https://hack.cert.pl/challenge/mind-blank)

Server seed is created based on some unknown hardcoded string and known time with precision down to the second:
```python
ts = time.ctime(time.time())
print(f"{ts} can you read my mind?")
random.seed(hmac.digest(b'SOME_SECRET_YOU_DONT_HAVE', str(ts).encode(), digest='sha256'))
```
Taps and state for LFSR are generated randomly using this seed. So approach is to establish multiple connections to the server at the same second (to have the same seed set) to increase probability of guessing state: [guessing_state.py](guessing_state.py).

Having state and 48 bits produced by LFSR, we can brute force taps (takes about 1 second) and decrypt the flag received from the server: [sol.py](sol.py).

### Flag
```
ecsc23{I_see_we_got_ourselves_a_mind_reader_here}
```
