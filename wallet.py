import ecdsa
import json
import os
from binascii import hexlify, unhexlify

import settings
from crypto import encode_data
from blockchain import TransactionBlock

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

    def make_transaction(self, recipient_public_key, previous_block):
        trans_block = TransactionBlock(
                previous_block,
                self.public_key,
                recipient_public_key,
                self.sign_transaction(recipient_public_key, previous_block))
        return trans_block 

    def sign_transaction(self, recipient_public_key, previous_block):
        try:
            data = (recipient_public_key, previous_block.generate_hash())
        # if the prev block is something unexpected
        except AttributeError:
            data = (recipient_public_key, None)
        encoded_data = encode_data(data)
        signature = self.secret_key.sign(encoded_data)
        return signature
    
    def save_key(self, wallet_name, key_type): 
        if key_type == 'public_key':
            key = self.public_key
            key_path = os.path.join(settings.WALLETS_ABS_PATH, wallet_name + ".pk" )

        elif key_type == 'secret_key':
            key = self.secret_key
            key_path = os.path.join(settings.WALLETS_ABS_PATH, wallet_name + ".sk" )

        else:
            raise ValueError('Third argument key_type needs to be either public_key or secret_key.')

        with open(key_path, 'wb') as temp_file:
            hex_key = hexlify(key.to_string())
            temp_file.write(hex_key)

    def save_public_key(self, wallet_name):
        self.save_key(wallet_name, 'public_key')
        print("Public key saved.")

    def save_secret_key(self, wallet_name):
        self.save_key(wallet_name, 'secret_key')
        print("Secret key saved.")

    def save_wallet(self, wallet_name):
        self.save_public_key(wallet_name)
        self.save_secret_key(wallet_name)

    @classmethod
    def load_key(cls, wallet_name, key_type):
        if key_type == 'public_key':
            ecdsa_key = ecdsa.VerifyingKey
            extension = ".pk"
        elif key_type =='secret_key':
            ecdsa_key = ecdsa.SigningKey
            extension = ".sk"
        else:
            raise ValueError('Third argument key_type needs to be either public_key or secret_key.')
        
        key_path = os.path.join(settings.WALLETS_ABS_PATH, wallet_name + extension)
        with open(key_path, 'rb') as temp_file:
            hex_key = temp_file.read()
            bytes_key = unhexlify(hex_key)
            key = ecdsa_key.from_string(bytes_key, settings.bitcoin_curve)

        return key 

    @classmethod
    def load_public_key(cls, wallet_name):
        return cls.load_key(wallet_name, 'public_key')
        print("Public key loaded.")

    @classmethod
    def load_secret_key(cls, wallet_name):
        return cls.load_key(wallet_name, 'secret_key')
        print("Secret key loaded.")

    @classmethod
    def load_wallet(cls, wallet_name):
        secret_key = cls.load_secret_key(wallet_name)
        public_key = cls.load_public_key(wallet_name)
        return Wallet(secret_key, public_key)

    @classmethod
    def deprecated_load(cls, wallet_name): #cls stands for class, because the variable name class is taken
        with open(wallet_name, 'rb') as temp_file:
            temp_array = temp_file.read().splitlines()
            secret_key_hex, public_key_hex = temp_array 
            secret_key_bytes, public_key_bytes = unhexlify(secret_key_hex), unhexlify(public_key_hex)
            secret_key, public_key = ecdsa.SigningKey.from_string(secret_key_bytes, settings.bitcoin_curve), ecdsa.VerifyingKey.from_string(public_key_bytes, settings.bitcoin_curve)
            print("Wallet loaded.")
            return Wallet(secret_key, public_key) 
