import pytest
import ecdsa
import random
from binascii import hexlify, unhexlify
import os

import settings
from crypto import encode_data
from wallet import Wallet

# Wallet tests
alice = Wallet()
def test_wallet_init():
    assert len(alice.secret_key.to_string()) == 32
    assert len(alice.public_key.to_string()) == 64

def test_wallet_str():
    pass
    # parse public key, secret key

def test_sign_transaction():
    message = encode_data(("bob", "123"))
    sign = alice.sign_transaction("bob", "123")
    assert alice.public_key.verify(sign, message)

def test_save_key():
    wallet_name = "test_save_key"
    key_path = os.path.join(settings.WALLETS_ABS_PATH, wallet_name + ".pk")
    try:
        os.remove(key_path)
    except OSError:
        pass

    alice.save_key(wallet_name, "public_key")
    assert os.path.isfile(key_path)
    with open(key_path, "rb") as test_file:
        hex_key = test_file.read()
        unhexlify(hex_key)

    key_path = os.path.join(settings.WALLETS_ABS_PATH, wallet_name + ".sk")
    try:
        os.remove(key_path)
    except OSError:
        pass
    
    alice.save_key(wallet_name, "secret_key")
    assert os.path.isfile(key_path)
    with open(key_path, "rb") as test_file:
        hex_key = test_file.read()
        unhexlify(hex_key)

    with pytest.raises(ValueError):
        alice.save_key(wallet_name, "bla")

def test_save_public_key():
    wallet_name = "test_save_pk"
    key_path = os.path.join(settings.WALLETS_ABS_PATH, wallet_name + ".pk")
    try:
        os.remove(key_path)
    except OSError:
        pass
    
    alice.save_key(wallet_name, "public_key")
    assert os.path.isfile(key_path)
    
def test_save_secret_key():
    wallet_name = "test_save_sk"
    key_path = os.path.join(settings.WALLETS_ABS_PATH, wallet_name + ".sk")
    try:
        os.remove(key_path)
    except OSError:
        pass
    
    alice.save_key(wallet_name, "secret_key")
    assert os.path.isfile(key_path)

def test_save_wallet():
    wallet_name = "test_save_wallet"
    public_key_path = os.path.join(settings.WALLETS_ABS_PATH, wallet_name + ".pk")
    secret_key_path = os.path.join(settings.WALLETS_ABS_PATH, wallet_name + ".sk")
    try:
        os.remove(public_key_path)
        os.remove(secret_key_path)
    except OSError:
        pass

    alice.save_wallet(wallet_name)
    assert os.path.isfile(public_key_path)
    assert os.path.isfile(secret_key_path)

def test_load_key():
    wallet_name = "test_load_key"
    alice.save_public_key(wallet_name)
    alice.save_secret_key(wallet_name)
    
    expected_pk = Wallet.load_key(wallet_name, "public_key")
    assert alice.public_key.to_string() == expected_pk.to_string()
    
    expected_sk = Wallet.load_key(wallet_name, "secret_key")
    assert alice.secret_key.to_string() == expected_sk.to_string()

def test_load_public_key():
    wallet_name = "test_load_pk"
    alice.save_public_key(wallet_name)

    expected_pk = Wallet.load_public_key(wallet_name)
    assert alice.public_key.to_string() == expected_pk.to_string()

def test_load_secret_key():
    wallet_name = "test_load_sk"
    alice.save_secret_key(wallet_name)

    expected_sk = Wallet.load_secret_key(wallet_name)
    assert alice.secret_key.to_string() == expected_sk.to_string() 

def test_wallet():
    test_wallet_init()
    test_wallet_str()
    test_sign_transaction()
    test_save_key()
    test_save_public_key()
    test_save_secret_key
    test_save_wallet()

test_wallet()
