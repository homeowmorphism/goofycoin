from wallet import *
from goofycoin import *
from goofy import *
from binascii import hexlify

# wallet.py tests 
print("Testing wallet.py...")

anna = Wallet()
anna.save_wallet('anna.txt')
anna_copy = Wallet.load('anna.txt')
assert anna.secret_key.to_string() == anna_copy.secret_key.to_string()
assert anna.public_key.to_string() == anna_copy.public_key.to_string()

bob = Wallet.load('bob.txt')
assert str(bob) == 'secret key: 9f04dcc770eb29a4323b4d43de2b6cc8d258104379efeef7c36643fece996f96 \n public key: deea6364bb4445106eee6707815e6c8138bc08c6ca8d927235390c6519df9800aa52a80c6ec7665659ec47fb549e980c73d5d0fc6b13b528cb685d112f935871'

print("All wallet.py tests have passed.")

# goofy.py tests 

print("Testing goofy.py...")

assert isinstance(goofy, Wallet) == True

hexlify(goofy.secret_key.to_string()), b'7faa2bd3924ecbb89ac917dbb5d28667aafe5db9918aa04a5fbd1881ed6e8500'

coin = goofy.make_coin()
print(coin)

# test Goofycoin file
## load goofy
assert b'fb50747be4f1daacef9ff080be3ccac8dea4a30f3ced57bdbc020985eeb7ca07a136caaa58a7eda1d3e8f2733fc01832d6fd0bbccbc3294e942b88826911068f',(hexlify(goofy.public_key.to_string()))

## Coin(object)
coin = goofy.make_coin()
assert '2bZcPUkdCaHuTfhdgGS4Cz96AAv4S5vqWaeHYH8YGUCXAxa5eXNSwbFTcpaAkK6JULZp7J1wj7LoFYACTooKYd2F7aAjiqJkvq1qJSjrnbA', str(coin)

signature = goofy.sign_transfer_coin(coin, anna.public_key)
assert b'=\xa5)\x01\xe2p\x9b0\xa0\xbfO\x08\xfe>Q\x10\xea\xf1^\xbb\xe5K\xdet\xe7\x12\xf1j\xb02\x11\xef\x07\xa5Ij\xe3\x7f\xe3\xc0\xd0\x913\x06\x18\xa2\xa7\x1a\xb5\x9c\xd2\x11\xed,-\xb6\x8aND\xe2\xb4\x8eq]', signature 

first_transaction = make_coin_transfer(coin, anna.public_key, signature)
first_transaction.verify_chain()
print(first_transaction.hash)

second_transaction = TransactionBlock(first_transaction, first_transaction.hash, anna.public_key, bailey.public_key, anna.sign_transaction(bailey.public_key, first_transaction.hash)) 
second_transaction.verify_chain()

second_transaction = TransactionBlock(first_transaction, first_transaction.hash, goofy.public_key, bailey.public_key, anna.sign_transaction(bailey.public_key, first_transaction.hash)) 
second_transaction.verify_chain()
