# coding=utf-8

from Crypto.Hash import SHA256
from Crypto import Random

def execute_encryption(is_encryption, input_word):
    executed_word = ''
    if is_encryption:
        hash_sha256 = SHA256.new()
        hash_sha256.update(input_word)
        executed_word = hash_sha512.hexdigest()
    else:
        executed_word = private_key.decrypt(input_word)

    return executed_word
