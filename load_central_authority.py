import settings

from wallet import Wallet

def load_goofy_public_key():
    goofy_public_key = Wallet.load_public_key(settings.GOOFY_PK_FILE) 
    return goofy_public_key 
