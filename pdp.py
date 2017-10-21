# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto import Random
import binascii
import sys,os
import dbm
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA

class PDP(object):

    #获得RSA的参数
    def __init__(self):
        # 伪随机数生成器
        random_generator = Random.new().read
        # rsa算法生成实例
        rsa = RSA.generate(1024, random_generator)
        # 秘钥对的生成
        private_pem = rsa.exportKey()
        with open('private.pem', 'w') as f:
            f.write(private_pem)

        public_pem = rsa.publickey().exportKey()
        with open('public.pem', 'w') as f:
            f.write(public_pem)

        print 'N=', rsa.n
        print 'e=', rsa.e
        print 'd=', rsa.d
        print 'u=', rsa.u

    #文件分块
    def split(self, fromfile,todir, chunksize = 1):
        if not os.path.exists(todir):#check whether todir exists or not
            os.mkdir(todir)
        else:
            for fname in os.listdir(todir):
                os.remove(os.path.join(todir,fname))
        partnum = 0
        inputfile = open(fromfile,'rb') #open the fromfile
        while True:
            chunk = inputfile.read(chunksize * 1024)
            if not chunk:             #check the chunk is empty
                break
            partnum += 1
            filename = os.path.join(todir, ('part%02d' % partnum))
            fileobj = open(filename,'wb') #make partfile
            fileobj.write(chunk)         #write data into partfile
            fileobj.close()
        return partnum

    def doSplit(self):
        # fromfile  = input('输入待分块文件路径：')
        # todir     = input('输入保存分块文件路径：')
        fromfile  = "/home/lfq/pdp/c_ca-certificates.conf"
        todir     = "/home/lfq/pdp/splitFile"
        # chunksize = int(input('输入分块大小（KB）：'))
        chunksize = 2
        absfrom,absto = map(os.path.abspath,[fromfile,todir])
        print('Splitting',absfrom,'to',absto,'by',chunksize)
        try:
            parts = self.split(fromfile,todir,chunksize)
        except:
            print('Error during split:')
            print(sys.exc_info()[0],sys.exc_info()[1])
        else:
            print('split finished:',parts,'parts are in',absto)

    def joinfile(self):
        fromdir  = "/home/lfq/pdp/splitFile"
        todir     = "/home/lfq/pdp/joinFile"
        if not os.path.exists(todir):
            os.mkdir(todir)
        if not os.path.exists(fromdir):
            print('Wrong directory')
        outfile = open(os.path.join(todir,"c_ca-certificates.conf"),'wb')
        files = os.listdir(fromdir) #list all the part files in the directory
        files.sort()                #sort part files to read in order
        for file in files:
            filepath = os.path.join(fromdir,file)
            infile = open(filepath,'rb')
            data = infile.read()
            outfile.write(data)
            infile.close()
        outfile.close()

    def AES_File(self, msg):

        H = MD5.new()
        H.update(msg)
        key = H.hexdigest() #16-bytes password
        print "key=", key

        iv = Random.new().read(AES.block_size)
        print "iv=", binascii.b2a_hex(iv)
        #保存key, iv值到文件
        db = dbm.open('fiv', 'c')
        db['key'] = key
        db['iv'] = iv
        db.close()

        cipher = AES.new(key, AES.MODE_CBC, iv)

        x = len(msg) % 16
        print "明文长度：", len(msg)
        print '填充长度: ', 16-x
        msg_pad = msg
        if x != 0:
            msg_pad = msg + '0'*(16 - x)
        # emsg = binascii.b2a_hex(iv+cipher.encrypt(msg_pad))
        emsg = cipher.encrypt(msg_pad)
        return emsg

    def DAES_File(self, csg):

        db = dbm.open('fiv', 'r')
        key = db['key']
        iv = db['iv']
        db.close()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        msg = cipher.decrypt(csg)

        return msg

    def doEncrypt(self):

        fm = open('ca-certificates.conf', 'r+')
        m = fm.read()
        fm.seek(0,0)
        fm.close()

        #Crypt Src FileStream
        fc = open('c_ca-certificates.conf', 'wb')
        c = self.AES_File(m)
        fc.write(c)
        fc.close()

    def doDecrypt(self):

        fc = open('joinFile/c_ca-certificates.conf', 'r+')
        c = fc.read()
        fc.seek(0,0)
        fc.close()

        #Crypt Src FileStream
        fm = open('joinFile/ca-certificates.conf', 'wb')
        m = self.DAES_File(c).rstrip('0')
        fm.write(m)
        fm.close()

        fm0 = open('ca-certificates.conf', 'r+')
        m0 = fm0.read()
        fm0.seek(0,0)
        fm0.close()

        if m == m0:
            print "解密成功！"
        else:
            print "解密失败！"

if __name__ == '__main__':

    pdp = PDP()
    # pdp.doEncrypt()
    # pdp.doSplit()
    # pdp.joinfile()
    # pdp.doDecrypt()

