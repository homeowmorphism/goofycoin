import os
from binascii import unhexlify
import ecdsa

import settings

class ExternalUser():
    def __init__(self, username):
        self.public_key = load_external(username) 
    def load_external(username):
        public_key_path = os.path.join(settings.EXTERNAL_REL_PATH, username + ".pk")
        with open(public_key_path, 'rb') as temp_file:
            hex_key = temp_file.read()
            bytes_key = unhexlify(hex_key)
            public_key = ecdsa.VerifyingKey.from_string(bytes_key, settings.bitcoin_curve)
        return public_key 

    @classmethod
    def load_goofy_public_key(cls):
        goofy_public_key = cls.load_external(settings.GOOFY_PK_FILE) 
        return goofy_public_key 
