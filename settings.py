import ecdsa
import os

SCRIPT_DIRECTORY = os.path.dirname(__file__)
WALLETS_REL_PATH = 'wallets'
WALLETS_ABS_PATH = os.path.join(SCRIPT_DIRECTORY, WALLETS_REL_PATH)
EXTERNAL_REL_PATH = 'external-users'
EXTERNAL_ABS_PATH = os.path.join(SCRIPT_DIRECTORY, EXTERNAL_REL_PATH)
GOOFY_PK_FILE = os.path.join(EXTERNAL_ABS_PATH, "goofy")
GOOFY_FILENAME = "goofy"

bitcoin_curve = ecdsa.SECP256k1
coin_id_size = 256

