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

