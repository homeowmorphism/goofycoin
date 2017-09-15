from hashlib import sha256
import ecdsa
from binascii import hexlify
import random 
import base58
import json

import goofycoin.settings 
from goofycoin.crypto import encode_data
from goofycoin.external import ExternalUser 
from goofycoin.coin import Coin

# in this scheme, every transaction is a block
class TransactionBlock(object):
    def __init__(self, previous_block, spender_public_key,  recipient_public_key, signature):
        self.previous_block = previous_block

        try:
            self.previous_hash = previous_block.generate_hash() 
        # in case there is no previous block
        except AttributeError:
            self.previous_hash = None

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
     
    def chain_is_authentic(self):
        try:
            goofy_public_key = ExternalUser.load_goofy_public_key()
            signature_to_check = encode_data((self.recipient_public_key, self.previous_hash))

            if isinstance(self.previous_block,Coin):
                if (goofy_public_key.verify(self.previous_block.signature, str(self.previous_block.coin_id).encode()) and  
                goofy_public_key.verify(self.signature, json.dumps((str(self.recipient_public_key),str(self.previous_block.coin_id))).encode())): 
                    return True
                else: 
                    return False

            elif isinstance(self.previous_block, TransactionBlock):
                if (self.previous_hash == self.previous_block.hash and 
                self.spender_public_key == self.previous_block.recipient_public_key):
                        self.spender_public_key.verify(self.signature, signature_to_check)
                        return self.previous_block.chain_is_authentic() 
                else:
                    print("Transactions " + str(self.hash) + " and " + str(self.previous_block.hash) + " do not match.") 

            else: 
                print("Types do not match up in the chain.")

        except ecdsa.BadSignatureError:
            return False

    def to_list_entry():
        return {
                "previous_hash":        self.previous_hash, 
                "spender_public_key":   self.spender_public_key 
                "recipient_public_key": self.recipient_public_key
                "signature":            self.signature
                "hash":                 self.hash 
                }
