# 34C3 CTF 2017: JuniorCTF - Kim

**Category:** Cryptography
**Description:**

> Check 35.198.133.163:1337 out!!!!!!!!!!!\x80\x00....
>
> [kim.py](kim.py)

## Write-up

Ketika kita membuka link yang diberikan, didapatkan halaman dengan sebuah link Download file yang mengarahkan ke link `http://35.198.133.163:1337/files/952bb2a215b032abe27d24296be099dc3334755c/?f=sample.gif`

Tujuan dari soal ini adalah untuk mendapatkan file flag dengan nilai umac yang tepat
`http://url/files/{{mac}}/?f={{file}}`

```python
@route('/files/<umac>/')
def download(umac):
    delim = msg = ''
    for k,v in request.query.allitems():
        msg += delim + k + '=' + v
        delim = '&'
    if mac(msg) == umac:
        return static_file(request.query.f, root='./files')
    else:
        return redirect('/files/' + mac('f=dont.gif') + '/?f=dont.gif')
```

Setelah menganalisa ternyata didapatkan 3 buah file pada directory files/`http://35.198.133.163:1337/files/`
* sample.gif
* dont.gif
* flag

Ternyata didapatkan fungsi untuk generate umac vulnerable terhadap karena memakai sha1 untuk [Length Extension Attack](https://en.wikipedia.org/wiki/Length_extension_attack)

```python
def mac(msg):
    return hashlib.sha1(SECRET + msg).hexdigest()
```

Fungsi hash kriptografis yang vulnerable terhadap serangan ini adalah fungsi hash yang menggunakan struktur Merkle-Damgard seperti MD5, SHA1, SHA2.

Secara sederhana hash length extension attack bisa digambarkan sebagai berikut:
Bila diketahui data dan nilai hash dari (secret + data), maka kita bisa menghitung hash dari (secret + data + datatambahan) walaupun tidak mengetahui secret.
Untuk lebih lengkapnya bisa dibaca [disini](http://www.ilmuhacking.com/cryptography/mengeksploitasi-hash-length-extension/)

### Exploit
Kita memakai fungsi dari [hlextend](https://github.com/stephenbradshaw/hlextend)

Kita perlu tau panjang dari secret untuk mendapatkan hash dan data yang tepat
yang bisa dilakukan adalah dengan pendekatan bruteforce

[solver.py](solver.py)

```bash
$ python solver.py 
Content-Length= 1023227, key-length= 1, url= http://35.198.133.163:1337/files/a93fa768ea2a83382912f7259fb676d75d95d243/?f=dont.gif%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00H&f=flag
Content-Length= 1023227, key-length= 2, url= http://35.198.133.163:1337/files/a93fa768ea2a83382912f7259fb676d75d95d243/?f=dont.gif%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00P&f=flag
...
...
Content-Length= 35, key-length= 17, url= http://35.198.133.163:1337/files/a93fa768ea2a83382912f7259fb676d75d95d243/?f=dont.gif%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%C8&f=flag
...
...
```

Kita dapatkan pada `key-length=17` mempunyai `Content-Length` yang berbeda

```bash
$ curl -v "http://35.198.133.163:1337/files/a93fa768ea2a83382912f7259fb676d75d95d243/?f=dont.gif%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%C8&f=flag"
* Hostname was NOT found in DNS cache
*   Trying 35.198.133.163...
* Connected to 35.198.133.163 (35.198.133.163) port 1337 (#0)
> GET /files/a93fa768ea2a83382912f7259fb676d75d95d243/?f=dont.gif%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%C8&f=flag HTTP/1.1
> User-Agent: curl/7.35.0
> Host: 35.198.133.163:1337
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Server: PasteWSGIServer/0.5 Python/2.7.14
< Date: Sat, 30 Dec 2017 11:35:21 GMT
< Last-Modified: Sat, 23 Dec 2017 16:25:30 GMT
< Content-Length: 35
< Accept-Ranges: bytes
< Content-Type: text/html; charset=UTF-8
< 
34C3_a11_y0u_ne3d_is_puMp_and_dump
* Closing connection 0
```

## References

* [hlextend](https://github.com/stephenbradshaw/hlextend)
* [rentjong](http://blog.rentjong.net/2014/04/plaidctf2014-write-up-mtpox-web150.html)
* [ilmuhacking](http://www.ilmuhacking.com/cryptography/mengeksploitasi-hash-length-extension/)
