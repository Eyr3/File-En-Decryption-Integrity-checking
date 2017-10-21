#-*- coding: utf-8 -*-

import hashlib
import rsa

def get_W_sha1(W):
        myhash = hashlib.sha1()
        myhash.update(W)
        return hashlib.sha1().hexdigest()

def import_key():
        with open('public.pem', 'r') as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
        with open('private.pem', 'r') as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())
        n = pubkey.n
        e = privkey.e
        d = privkey.d
        g = e
        return n, e, d, g

def get_c(file_name):
        with open(file_name + '.txt', 'r') as f:
            content = f.read()
        f.close()
        # list存入文件后，再次读取为list
        c = eval(content)
        return c

n, e, d, g = import_key()
s = 7 #随机取
chal = [1, 3, 5]
T_p = 1
M_s = 0

T = get_c('T')
for i in chal:
    T_p = T_p * int(T[i])
print T_p

M = get_c('M')
for i in chal:
    M_s = M_s + int(M[i])

p = get_W_sha1( str( pow( pow(g, s), M_s, n)) )
print p


'''
https://zhidao.baidu.com/question/393434693667477365.html
'''