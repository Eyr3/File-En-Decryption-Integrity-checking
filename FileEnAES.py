#-*- coding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex, a2b_hex

import hashlib
import rsa
import random

#AES接口
class crypt():
    def __init__(self):
        self.key = '1234567890123456'
        self.iv = Random.new().read(AES.block_size) #'This is an IV456'
        self.mode = AES.MODE_CBC
        self.BS = AES.block_size
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    def encrypt(self, text):
        text = self.pad(text)
        self.obj1 = AES.new(self.key, self.mode, self.iv)
        self.ciphertext = self.obj1.encrypt(text)
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        self.obj2 = AES.new(self.key, self.mode, self.iv)
        plain_text = self.obj2.decrypt(a2b_hex(text))
        return self.unpad(plain_text.rstrip('\0'))

if __name__ == '__main__':
    pc = crypt()
    def get_W_sha1(W):
        myhash = hashlib.sha1()
        myhash.update(W)
        return hashlib.sha1().hexdigest()

    def get_file_m(file_name):
        with open(file_name, 'rb') as f:
            fs = f.read()
            m = pc.encrypt(fs)
        return m

    # 保存密钥
    def save_key():
        (pubkey, privkey) = rsa.newkeys(1024)
        with open('public.pem', 'w+') as f:
            f.write(pubkey.save_pkcs1().decode())
        with open('private.pem', 'w+') as f:
            f.write(privkey.save_pkcs1().decode())

    # 导入密钥,并返回n,e,d,g
    def import_key():
        with open('public.pem', 'r') as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
        with open('private.pem', 'r') as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())
        n = pubkey.n
        e = privkey.e
        d = privkey.d
        g = 3
        return n, e, d, g

    filename = 'test.txt'
    T = []
    M = []
    save_key()
    n, e, d, g = import_key()
    print n
    print e
    print d
    print g

    for i in range(0, 8):
        m = get_file_m(filename + '_split_'+ str(i) + '.txt')
        #d = pc.decrypt(m)
        #print 'd = '+d
        m = int(m, 16)  # 16进制字符转数字：int('1a', 16)
        M.append(m)
        W = '11' + str(i) #暂定 W=v||i, v='11'

        h_W = int(get_W_sha1(W), 16)
        T.append( pow( pow(h_W, d, n) * pow(g, m*d, n) , 1, n ) )
        #print 'len(T) = %d' % len(str(T))
    with open('M.txt', 'w') as f:
        f.write(str(M))
    with open('T.txt', 'w') as f:
        f.write(str(T))
    f.close()

'''
http://blog.csdn.net/qq_30391343/article/details/50433668
'''