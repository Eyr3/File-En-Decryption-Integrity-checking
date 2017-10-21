#-*- coding: utf-8 -*-
import hashlib
import random

def get_W_sha1(W):
    myhash = hashlib.sha1()
    myhash.update(W)
    return hashlib.sha1().hexdigest()

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

h_p = 1
chal = [1, 3, 5]
s = 7 #random.randint(1000, 1000000)

for i in chal:
    W = '65537' + str(i)
    h_W = int(get_W_sha1(W), 16)
    h_p = h_p * h_W
print len(str(h_p))

t = (pow(T, e, n)* modinv(h_p, n)) % n

print t
#t = pow(T, e, n) % pow(h_p, 1, n)
#t = pow( pow(T, e) / h_p, 1, n)

p_S = 0xda39a3ee5e6b4b0d3255bfef95601890afd80709
p_C = get_W_sha1(str( pow(t, s, n)))
if p_C == p_S :
    print 'success'
else:
    print 'failure'