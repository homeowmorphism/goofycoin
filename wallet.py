import ecdsa
import json
import dill

class Wallet(object):
    def __init__(self, sk = None, pk = None):
        if sk == None:
            self.sk = ecdsa.SigningKey.generate(ecdsa.SECP256k1)
            self.pk = self.sk.get_verifying_key()
        else:
            self.sk = sk
            self.pk = pk

    def __str__(self):
        return "(" + str(hexlify(self.sk.to_string())) + "," + str(hexlify(self.pk.to_string())) + ")"

    def sign_transaction(self, recipient_pk, previous_hash):
        return self.sk.sign(json.dumps((str(recipient_pk),str(previous_hash))).encode())

def save_wallet(wallet, filename):
        with open(filename + '.pkl', 'wb') as file:
            dill.dump(wallet, file)

def load_wallet(filename):
    with open(filename + '.pkl', 'rb') as file:
        print("Wallet loaded.")
        return dill.load(file)
