import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pyDes import des, CBC, PAD_PKCS5


def encrypt_des_cbc(text, key, iv):
    """
    encrypt_des_cbc
    """
    des_obj = des(
        key[:8].encode("utf-8"), CBC, iv.encode("utf-8"), pad=None, padmode=PAD_PKCS5
    )
    encrypt_text = des_obj.encrypt(text)
    encrypt_text = base64.encodebytes(encrypt_text).decode("utf-8").replace("\n", "")
    return encrypt_text


def decrypt_des_cbc(text: str, key: str, iv: str) -> str:
    """
    decrypt_des_cbc
    """
    decode_encrypt_text = base64.b64decode(text)
    des_obj = des(
        key[:8].encode("utf-8"), CBC, iv.encode("utf-8"), pad=None, padmode=PAD_PKCS5
    )
    decrypt_text = des_obj.decrypt(decode_encrypt_text, padmode=PAD_PKCS5).decode(
        "utf8"
    )
    return decrypt_text


# e = 'φρϛύπ'
def decrypt_xor(e):
    """
        xor
    :param e:
    :return:
    """
    decode = ""
    for i in e:
        a = 1013 ^ ord(i)
        decode += chr(a)
    return decode


def get_sign(params, app_key):
    """

    :param params:
    :return:
    """
    sign_str = ""
    for key, value in sorted(params.items(), key=lambda x: x[0]):
        sign_str += key + value
    sign_str = app_key + sign_str + app_key
    sign = hashlib.md5(sign_str.encode(encoding="utf-8")).hexdigest()
    return sign


def encrypt_ascii(e):
    """
        encrypt_ascii
    """
    result = ""
    for i in e:
        result += hex(5 ^ ord(i))[2:]
    return result


def decode_ascii(e):
    """
        decode_ascii
    """
    e = [e[i : i + 2] for i in range(0, len(e), 2)]
    result = ""
    for i in e:
        a = int(i, 16)
        result += chr(5 ^ a)
    return result


def encrypt_aes_cbc(text, key, iv):
    """
    encrypt_aes_cbc
    """
    aes = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    encrypt_text = aes.encrypt(pad(text.encode("utf-8"), AES.block_size, style="pkcs7"))
    return encrypt_text.hex()


def decrypt_aes_cbc(text, key, iv):
    """
        decrypt_aes_cbc
    """
    enc = bytes.fromhex(text)
    aes = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    encrypt_text = aes.decrypt(enc)
    return unpad(encrypt_text, AES.block_size, style="pkcs7").decode("utf-8")
