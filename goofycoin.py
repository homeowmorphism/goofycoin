from hashlib import sha256
import ecdsa
from binascii import hexlify
import random 
import base58
import json
import dill

#load central authority's pk
with open('goofy-pk.pkl', 'rb') as file:
    goofy_pk = dill.load(file)

class Coin(object):
    def __init__(self, coin_id, signature):
        self.coin_id = coin_id 
        self.signature = signature

    def __str__(self):
        return self.coin_id

    def verify(self):
        try: 
            goofy_pk.verify(self.signature, str(self.coin_id).encode())
            print("Coin is authentic.")
        except ecdsa.keys.BadSignatureError:
            print("Coin is fake.")

class TransactionBlock(object):
    def __init__(self, previous_transaction, previous_hash, spender_pk,  recipient_pk, signature):
        self.previous_transaction = previous_transaction
        self.previous_hash = previous_hash
        self.spender_pk = spender_pk
        self.recipient_pk = recipient_pk
        self.signature = signature 
        self.hash = self.generate_hash() 

    def __str__(self):
        return "(" + str(hexlify(self.spender_pk.to_string())) + "," + str((self.recipient_pk.to_string())) + "," + str(self.hash) + ")"
    
    def generate_hash(self):
        hash_content = "(" + str(self.previous_transaction) + "," + str(self.previous_hash) + "," + str(self.recipient_pk) + ")" 
        hash_function = sha256()
        hash_function.update(hash_content.encode())
        return hash_function.hexdigest()
     
    def verify_chain(self):
        if isinstance(self.previous_transaction,Coin):
            if goofy_pk.verify(self.previous_transaction.signature, str(self.previous_transaction.coin_id).encode()) and goofy_pk.verify(self.signature, json.dumps((str(self.recipient_pk),str(self.previous_transaction.coin_id))).encode()): 
                print("Chain is authentic.")
            else: 
                print("Chain has been tempered with.")
        elif isinstance(self.previous_transaction, TransactionBlock):
            if self.previous_hash == self.previous_transaction.hash and self.spender_pk == self.previous_transaction.recipient_pk:
                print(self.spender_pk)
                print(self.previous_transaction.recipient_pk)
                return self.previous_transaction.verify_chain() 
            else:
                print("Transactions " + str(self.hash) + " and " + str(self.previous_transaction.hash) + " do not match.") 

        else: 
            print("Types do not match up in the chain.")

        

