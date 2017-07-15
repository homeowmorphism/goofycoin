import ecdsa
import json
import dill
from binascii import hexlify

class Wallet(object):
    def __init__(self, secret_key = None, public_key = None):
        if secret_key == None:
            self.secret_key = ecdsa.SigningKey.generate(ecdsa.SECP256k1)
            self.public_key = self.secret_key.get_verifying_key()
        else:
            self.secret_key = secret_key
            self.public_key = public_key

    def __str__(self):
        return "(" + str(hexlify(self.secret_key.to_string())) + "," + str(hexlify(self.public_key.to_string())) + ")"

    def sign_transaction(self, recipient_pk, previous_hash):
        return self.secret_key.sign(json.dumps((str(recipient_pk),str(previous_hash))).encode())

    @classmethod
    def load_wallet(cls, filename):
        with open(filename + '.pkl', 'rb') as file:
            print("Wallet loaded.")

def save_wallet(wallet, filename):
        with open(filename + '.pkl', 'wb') as file:
            dill.dump(wallet, file)
