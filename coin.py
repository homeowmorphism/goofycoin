import ecdsa

from load_central_authority import load_goofy_public_key

class Coin(object):
    def __init__(self, coin_id, signature):
        self.coin_id = coin_id 
        self.signature = signature

    def __str__(self):
        return str(self.coin_id) + " : " + self.verify()

    def verify(self):
        goofy_public_key = load_goofy_public_key()
        try: 
            goofy_public_key.verify(self.signature, str(self.coin_id).encode())
            return "Valid."
        except ecdsa.keys.BadSignatureError:
            return "Invalid, bad signature."
        except AssertionError:
            return "Invalid, no signature."

