# coding=utf-8

from simple_aes_cipher import AESCipher, generate_secret_key
import os

def execute_encryption(is_encryption, input_word):
    pass_phrase = os.environ.get('ENCRYPT_PASS_PHARSE')
    secret_key = generate_secret_key(pass_phrase)

    # Generate cipher
    cipher = AESCipher(secret_key)

    executed_word = ''
    if is_encryption:
        # Encryption
        executed_word = cipher.encrypt(input_word)
    else:
        # Dencryption
        if ' ' in input_word:
            input_word = input_word.replace(' ', '+')
        executed_word = cipher.decrypt(input_word)

    return executed_word
