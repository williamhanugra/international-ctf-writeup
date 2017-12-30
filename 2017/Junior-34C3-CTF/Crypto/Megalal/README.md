# 34C3 CTF 2017: JuniorCTF - Megalal

**Category:** Cryptography
**Description:**

> You can reach a strange authentication system here: nc 35.197.255.108 1337
I'm sure you know what you have to do.
>
> [megalal.py](megalal.py)

## Write-up

Ketika dijalankan service kita dihadapakan 2 pilihan:
1. Login
2. Register

Tujuan dari soal ini, kita harus login menggunakan access token dengan role `overlord`, access token bisa didapatkan hanya dengan cara melakukan Register.

```python
if __name__ == '__main__':
    print('What do you want to do?')
    print('[1] Login')
    print('[2] Register')
    choice = raw_input('> ')
    try:
        if choice == '1':
            login()
        elif choice == '2':
            register()
    except:
        print('something went wrong...')
```

Tetapi ketika register kita tidak bisa memasukkan input role `overlord`

```python
if role == 'overlord':
        print('nope, you\'re not the overlord...')
        return
    c = enc('%s#%s' % (username, role))
    token = '{:x}_{:x}'.format(c[0], c[1])

    print('Here is your access token:\n{}'.format(token))

```
Token adalah hasil dari gabungan dari name dan role dipisahkan dengan karakter `#` lalu di encrypt menggunakan elgamal.

Enkripsi Elgamal menghasilkan 2 angka, lalu 2 angka tersebut di convert kedalam hex dan digabungkan dengan karakter `_`

```python
def enc(m):
    M = int(binascii.hexlify(m), 16)
    assert len(bin(M)) < len(bin(p)), 'm too long'

    y = random.SystemRandom().randint(0, p-1)
    c1 = pow(g, y, p)
    c2 = (M * pow(h, y, p) ) % p 

    return c1, c2

def register():
    username = raw_input('Your username: ')
    role = raw_input('Your role: ')

    if role == 'overlord':
        print('nope, you\'re not the overlord...')
        return
    c = enc('%s#%s' % (username, role))
    token = '{:x}_{:x}'.format(c[0], c[1])

    print('Here is your access token:\n{}'.format(token))
```

Kita dapat temukan kelemahan dari Enkripsi ElGamal di [Wikipedia](https://en.wikipedia.org/wiki/ElGamal_encryption#Security)

```
ElGamal encryption is unconditionally malleable, and therefore is not secure under chosen ciphertext attack. For example, given an encryption ( C1 , C2 ) of some (possibly unknown) message m, one can easily construct a valid encryption ( C1 , 2*C2 ) of the message 2*m.
```

Disini berarti kita dapat menghasilkan karakter yang kita inginkan `#overlord` dengan melakukan 2 kali dekripsi

string `#overlord` jika di convert ke hex akan menghasilkan `0x236f7665726c6f7264`, ketika kita mengirimkan value byte yang dibagi 2 untuk dienkripsi dan kita kirimkan ulang dengan dikali dengan 2 untuk mendapatkan flag

```python
from pwn import *
import binascii

context.log_level='error'

chosen = int(binascii.hexlify("#overlord"), 16)
role = binascii.unhexlify("{:02x}".format((chosen/2)))

#STEP 1
p = remote("35.197.255.108", 1337)

p.recv()
p.recv()
p.sendline("2") #choose 2 for Registration
p.recv()
p.sendline("a") #send username
p.recv()
p.sendline(role) #send role
acces_token = p.recv().split("\n")[1]
c1,c2 = acces_token.split("_")
new_acces_token = '{}_{:02x}'.format(c1, int(c2, 16) * 2)

#STEP 2
p = remote("35.197.255.108", 1337)

print p.recv()
print p.recv()
p.sendline("1") #choose 1 for Login
print p.recv()
p.sendline(new_acces_token) #send new_acces_token
print p.recvall()
```

## References

* [Hackeriet](https://blog.hackeriet.no/attacking_elgamal_encryption/)
* [Wikipedia](https://en.wikipedia.org/wiki/ElGamal_encryption#Security)
