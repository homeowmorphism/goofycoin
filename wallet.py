import ecdsa
import json
import dill
from binascii import hexlify, unhexlify

from crypto import encode_data

bitcoin_curve = ecdsa.SECP256k1

# The problem is that I'm not converting in modes that are pure to python. I'm doing dill stuff which correspond to very different formats that seem to look the same right now. 

class Wallet(object):
    def __init__(self, secret_key = None, public_key = None):
        if secret_key is None:
            self.secret_key = ecdsa.SigningKey.generate(bitcoin_curve)
            self.public_key = self.secret_key.get_verifying_key()
        else:
            self.secret_key = secret_key
            self.public_key = public_key

    def __str__(self):
        hex_secret_key, hex_public_key = hexlify(self.secret_key.to_string()), hexlify(self.public_key.to_string())

        str_secret_key, str_public_key = hex_secret_key.decode("ascii"), hex_public_key.decode("ascii")
       
        return("secret key: " + str_secret_key + " \n " + "public key: " + str_public_key)

    def sign_transaction(self, recipient_public_key, previous_hash):
        data = (recipient_public_key, previous_hash)
        encoded_data = encode_data(data)
        signature = self.secret_key.sign(encoded_data)
        return signature

    def save_wallet(self, filename):
            with open(filename, 'wb') as temp_file:
                hex_secret_key = hexlify(self.secret_key.to_string())
                hex_public_key = hexlify(self.public_key.to_string())
                temp_file.write(hex_secret_key)
                temp_file.write(b'\n')
                temp_file.write(hex_public_key)
                

    @classmethod
    def load(cls, filename): #cls stands for class, because the variable name class is taken
        with open(filename, 'rb') as temp_file:
            print("Wallet loaded.")
            temp_array = temp_file.read().splitlines()
            secret_key_hex, public_key_hex = temp_array 
            secret_key_bytes, public_key_bytes = unhexlify(secret_key_hex), unhexlify(public_key_hex)
            secret_key, public_key = ecdsa.SigningKey.from_string(secret_key_bytes, bitcoin_curve), ecdsa.VerifyingKey.from_string(public_key_bytes, bitcoin_curve)
            return Wallet(secret_key, public_key) 
            
