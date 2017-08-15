# library functions
import ecdsa
import json
import os
from binascii import hexlify, unhexlify
# directory files
from crypto import encode_data
import settings

SCRIPT_DIRECTORY = os.path.dirname(__file__)
WALLETS_REL_PATH = 'wallets'
WALLETS_ABS_PATH = os.path.join(SCRIPT_DIRECTORY, WALLETS_REL_PATH)


class Wallet(object):
    def __init__(self, secret_key=None, public_key=None):
        if secret_key is None:
            self.secret_key = ecdsa.SigningKey.generate(settings.bitcoin_curve)
            self.public_key = self.secret_key.get_verifying_key()
        else:
            self.secret_key = secret_key
            self.public_key = public_key

    def __str__(self):
        hex_secret_key, hex_public_key = hexlify(
            self.secret_key.to_string()), hexlify(self.public_key.to_string())

        str_secret_key, str_public_key = hex_secret_key.decode(
            "ascii"), hex_public_key.decode("ascii")

        return("secret key: " + str_secret_key + " \n " + "public key: " + str_public_key)

    def sign_transaction(self, recipient_public_key, previous_hash):
        data = (recipient_public_key, previous_hash)
        encoded_data = encode_data(data)
        signature = self.secret_key.sign(encoded_data)
        return signature

   def save_key(self, filename, keytype): 
    
    def save_public_key(self, filename):
        public_key_path = os.path.join(wallets_abs_path, filename)
        with open(public_key_path, 'wb') as temp_file:
            hex_public_key = hexlify(self.public_key.to_string())
            temp_file.write(hex_secret_key)

    def save_secret_key(self, filename):
        with open(filename, 'wb') as temp_file:
            hex_secret_key = hexlify(self.secret_key.to_string())
            temp_file.write(hex_secret_key)

    def save_wallet(self, wallet_name):
        save_public_key(wallet_name+'-public_key.txt')
        save_private_key(wallet_name+'private_key.txt')
        print("Wallet saved.")


# LOAD IS BROKEN
    @classmethod
    def deprecated_load(cls, filename): #cls stands for class, because the variable name class is taken
        with open(filename, 'rb') as temp_file:
            temp_array = temp_file.read().splitlines()
            secret_key_hex, public_key_hex = temp_array 
            secret_key_bytes, public_key_bytes = unhexlify(secret_key_hex), unhexlify(public_key_hex)
            secret_key, public_key = ecdsa.SigningKey.from_string(secret_key_bytes, settings.bitcoin_curve), ecdsa.VerifyingKey.from_string(public_key_bytes, settings.bitcoin_curve)
            print("Wallet loaded.")
            return Wallet(secret_key, public_key) 
