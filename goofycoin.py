from hashlib import sha256
import ecdsa
from binascii import hexlify
import random 
import base58
import json

from crypto import encode_data

#load central operator public key
GOOFY_PK_FILE = None

class TransactionBlock(object):
    def __init__(self, previous_transaction, previous_hash, spender_public_key,  recipient_public_key, signature):
        self.previous_transaction = previous_transaction
        self.previous_hash = previous_hash
        self.spender_public_key = spender_public_key
        self.recipient_public_key = recipient_public_key
        self.signature = signature 
        self.hash = self.generate_hash() 

    def __str__(self):
        return str(hexlify(self.spender_public_key.to_string())) + "," + str((self.recipient_public_key.to_string())) + "," + str(self.hash) + ")"
    
    def generate_hash(self):
        hash_content = json.dumps((str(self.previous_transaction),str(self.previous_hash),str(self.recipient_public_key)))
        hash_function = sha256()
        hash_function.update(hash_content.encode())
        return hash_function.hexdigest()
     
    def verify_chain(self):
        signature_to_check = (self.recipient_public_key, self.previous_hash)

        if isinstance(self.previous_transaction,Coin):
            if goofy_public_key.verify(self.previous_transaction.signature, str(self.previous_transaction.coin_id).encode()) and goofy_public_key.verify(self.signature, json.dumps((str(self.recipient_public_key),str(self.previous_transaction.coin_id))).encode()): 
                print("Chain is authentic.")
            else: 
                print("Chain has been tempered with.")
        elif isinstance(self.previous_transaction, TransactionBlock):
            if self.previous_hash == self.previous_transaction.hash and self.spender_public_key == self.previous_transaction.recipient_public_key and self.spender_public_key.verify(self.signature, signature_to_check):
                
                return self.previous_transaction.verify_chain() 
            else:
                print("Transactions " + str(self.hash) + " and " + str(self.previous_transaction.hash) + " do not match.") 

        else: 
            print("Types do not match up in the chain.")

class ExternalUser(object):
    def __init__(self, public_key):
        self.public_key = public_key

    def save_public_key(self, filename):
        with open(filename, 'wb') as temp_file:
            hex_public_key = helixfy(self.public_key.to_string())
            temp_file.write(hex_public_key)
        
    @classmethod
    def public_key_load(cls, filename):
        with open(filename, 'rb') as temp_file:
            print("Public key loaded.")
            public_key_hex = temp_file.read()
            public_key_bytes = unhexlify(public_key_hex)
            public_key = ecdsa.SigningKey.from_string(public_key_bytes, settings.bitcoin_curve)
            return ExternalUser(public_key) 

user_goofy = ExternalUser.public_key_load(ExternalUser('goofy_public_key.txt'))

