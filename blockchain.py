from hashlib import sha256
import ecdsa
from binascii import hexlify
import random 
import base58
import json

from crypto import encode_data
import settings 
from load_central_authority import load_goofy_public_key

# in this scheme, every transaction is a block
class TransactionBlock(object):
    def __init__(self, previous_block, previous_hash, spender_public_key,  recipient_public_key, signature):
        self.previous_block = previous_block
        self.previous_hash = previous_hash
        self.spender_public_key = spender_public_key
        self.recipient_public_key = recipient_public_key
        self.signature = signature 
        self.hash = self.generate_hash() 

    def __str__(self):
        statement = "Spender: " + str(hexlify(self.spender_public_key.to_string())) + "\n"
        statement += "Recipient: " + str((self.recipient_public_key.to_string())) + "\n"
        statement += "Hash: " + str(self.hash)
        return statement
    
    def generate_hash(self):
        hash_content = json.dumps((str(self.previous_block),str(self.previous_hash),str(self.recipient_public_key)))
        hash_function = sha256()
        hash_function.update(hash_content.encode())
        return hash_function.hexdigest()
     
    def verify_chain(self):
        goofy_public_key = load_goofy_public_key()
        signature_to_check = (self.recipient_public_key, self.previous_hash)

        if isinstance(self.previous_block,Coin):
            if (goofy_public_key.verify(self.previous_block.signature, str(self.previous_block.coin_id).encode()) and  
            goofy_public_key.verify(self.signature, json.dumps((str(self.recipient_public_key),str(self.previous_block.coin_id))).encode())): 
                print("Chain is authentic.")
            else: 
                print("Chain has been tempered with.")
        elif isinstance(self.previous_block, TransactionBlock):
            if (self.previous_hash == self.previous_block.hash and 
            self.spender_public_key == self.previous_block.recipient_public_key and 
            self.spender_public_key.verify(self.signature, signature_to_check)):
                return self.previous_block.verify_chain() 
            else:
                print("Transactions " + str(self.hash) + " and " + str(self.previous_block.hash) + " do not match.") 

        else: 
            print("Types do not match up in the chain.")

class ExternalUser(object):
    def __init__(self, public_key, username):
        self.public_key = public_key

    def save_public_key(self, filename):
        with open(filename, 'wb') as temp_file:
            hex_public_key = helixfy(self.public_key.to_string())
            temp_file.write(hex_public_key)
        
    def public_key_load(cls, filename):
        with open(filename, 'rb') as temp_file:
            print("Public key loaded.")
            public_key_hex = temp_file.read()
            public_key_bytes = unhexlify(public_key_hex)
            public_key = ecdsa.SigningKey.from_string(public_key_bytes, settings.bitcoin_curve)
            return public_key

