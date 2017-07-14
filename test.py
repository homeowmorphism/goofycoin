from wallet import *
from goofycoin import *
from goofy import *

anna = load_wallet('anna')
bailey = Wallet()

print(anna.sk)
print(anna.pk)

print(bailey.sk)
print(bailey.pk)

print(goofy.sk)
print(goofy.pk)

coin = goofy.make_coin()
print(coin)

signature = goofy.sign_transfer_coin(coin, anna.pk)

first_transaction = make_coin_transfer(coin, anna.pk, signature)
first_transaction.verify_chain()
print(first_transaction.hash)

second_transaction = TransactionBlock(first_transaction, first_transaction.hash, anna.pk, bailey.pk, anna.sign_transaction(bailey.pk, first_transaction.hash)) 
second_transaction.verify_chain()

second_transaction = TransactionBlock(first_transaction, first_transaction.hash, goofy.pk, bailey.pk, anna.sign_transaction(bailey.pk, first_transaction.hash)) 
second_transaction.verify_chain()
