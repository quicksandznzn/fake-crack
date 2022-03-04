import base64
from pyDes import des, CBC, PAD_PKCS5
import hashlib

def des_cbc_encrypt_text(decrypt_text: str, key: str, iv: str) -> str:
    """
    加密DES_CBC明文
    :param decrypt_text: 明文
    :param key: 密钥
    :param iv: 密钥偏移量
    :return: 加密后的数据
    """
    des_obj = des(
        key[:8].encode("utf-8"), CBC, iv.encode("utf-8"), pad=None, padmode=PAD_PKCS5
    )
    encrypt_text = des_obj.encrypt(decrypt_text)
    encrypt_text = str(base64.encodebytes(encrypt_text), encoding="utf-8").replace(
        "\n", ""
    )
    return encrypt_text


def decrypt_des_cbc(encrypt_text: str, key: str, iv: str) -> str:
    """
    解密DES_CBC密文
    :param encrypt_text: 密文
    :param key: 秘钥
    :param iv:秘钥便宜量
    :return:解密后的数据
    """
    decode_encrypt_text = base64.b64decode(encrypt_text)
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