import binascii
from Crypto.Cipher import DES
from django.conf import settings

def hex2byte(hexstring): 
    s = []
    for ch in hexstring:
        if ch.lower() in '01234567890abcdef':
            s.append(ch)
        else:
            s.append('f')
    return ''.join(s)
           
def xor(*args):
    arg1 = args[0]
    for arg in args[1:]:
        s = []
        for i, ch in enumerate(arg):
            s.append(chr(ord(arg1[i]) ^ ord(ch)))
        arg1 = ''.join(s)
    return arg1

def get_main_key():
    key = settings.SECRET_KEY
    k = xor(binascii.a2b_hex(hex2byte(key[:16])), 
        binascii.a2b_hex(hex2byte(key[16:32])), 
        binascii.a2b_hex(hex2byte(key[32:48])))
    lmk = DES.new(k, DES.MODE_ECB)
    return lmk

def encrypt(word, key=None):
    if not key:
        key = get_main_key()
    w = (word + ' '*8)
    word = w[:len(w)/8*8]
    return binascii.b2a_hex(key.encrypt(word))

def decrypt(word, key=None):
    if not key:
        key = get_main_key()
    return key.decrypt(binascii.a2b_hex(word)).strip()

def main():
    a = "hello"
    b = encrypt(a)
    print b
    print decrypt(b)