# 34C3 CTF 2017: JuniorCTF - Kim

**Category:** Miscellaneous
**Description:**

> If you're a baby and know bash, try this:
nc 35.189.118.225 1337

## Write-up

Pada challenge ini kita diberikan sebuah bash shell yang agak restricted, tapi kita diharuskan untuk menjalankan program `get_flag`

```bash
baby> help

    Welcome to babaybash!

    This is a challenge where you find yourself in a bash-jail.

    You want to execute /get_flag to get the flag!

    But the following characters are banned:
        - a-z
        - *
        - ?
        - .
    
    Good luck!

```

Ternyata kita bisa memakai huruf kapital pada bash tersebut

ada banyak cara membuat huruf menjadi lowercase pada bash, baca [disini](https://stackoverflow.com/questions/2264428/converting-string-to-lower-case-in-bash)

Salah satu cara yang paling mungkin adalah dengan menggunakan `VARIABEL="/GET_FLAG";${VARIABEL,,}`

```bash
baby> VARIABEL="/GET_FLAG";${VARIABEL,,}
Usage: /get_flag gimme_FLAG_please
```
Kita modifikasi supaya bisa menjalankan program dengan argumennya
```bash
baby> HURUF1="/GET_FLAG GIMME_";HURUF2="_PLEASE";${HURUF1,,}FLAG${HURUF2,,}
Good job!

Here's your flag: 34C3_LoOks_lik3_y0U_are_nO_b4by_4ft3r_4ll


```

## References

* [k3ramas](http://k3ramas.blogspot.co.id/2017/12/34c3-junior-ctf.html)
* [stackoverflow](https://stackoverflow.com/questions/2264428/converting-string-to-lower-case-in-bash)