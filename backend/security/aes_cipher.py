from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from dotenv import dotenv_values

config = dotenv_values()


class AES_CIPHER_CBC:

    # Clave de 128 bits (16 bytes)
    AES_KEY: bytes
    # Vector de inicialización de 128 bits (16 bytes)
    AES_IV: bytes

    # AES: Bloque de 128 bits
    BLOCK_SIZE_AES: int = 16

    def __init__(self):
        """Inicializa las variables locales"""
        self.AES_KEY = config.get("AES_KEY", "quantumproxy-app").encode()
        self.AES_IV = config.get("AES_IV", "quantumproxy-app").encode()

    def cifrar(self, cadena: str):
        """
        Cifra la cadena pasada por parámetro y devuelve el texto cifrado en binario
        """
        cipher = AES.new(self.AES_KEY, AES.MODE_CBC, self.AES_IV)
        data = cadena.encode("utf-8")
        return cipher.encrypt(pad(data, self.BLOCK_SIZE_AES))

    def descifrar(self, cifrado: bytes):
        """
        Descifra el cifrado pasado por parámetro y lo devuelve descrifrado en texto plano
        """
        decipher = AES.new(self.AES_KEY, AES.MODE_CBC, self.AES_IV)
        return unpad(decipher.decrypt(cifrado), self.BLOCK_SIZE_AES).decode(
            "utf-8", "ignore"
        )


cipher = AES_CIPHER_CBC()


def encrypt_data(data: str):
    return cipher.cifrar(data)


def decrypt_data(ciphertext: bytes):
    return cipher.descifrar(ciphertext)
