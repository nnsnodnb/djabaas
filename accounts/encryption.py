# coding=utf-8

from Crypto.PublicKey import RSA
from Crypto import Random

import os.path

CREATE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/keys/'
rsa = RSA.generate(2048)

def create_private_key():
    if os.path.isfile(CREATE_DIR + 'private.pem') == False:
        private_pem = rsa.exportKey(format = 'PEM',
                                    passphrase = os.environ.get('PRIVATE_PEM_PASSWORD'))
        with open(CREATE_DIR + 'private.pem', 'wb') as f:
            f.write(private_pem)

def create_public_key():
    if os.path.isfile(CREATE_DIR + 'public.pem') == False:
        public_pem = rsa.publickey().exportKey()
        with open(CREATE_DIR + 'public.pem', 'wb') as f:
            f.write(public_pem)

def load_private_key():
    private_key_file = open(CREATE_DIR + 'private.pem', 'r')
    return RSA.importKey(private_key_file.read(),
                         passphrase = os.environ.get('PRIVATE_PEM_PASSWORD'))

def load_public_key():
    public_key_file = open(CREATE_DIR + 'public.pem', 'r')
    return RSA.importKey(public_key_file.read())

def execute_encryption(is_encryption, input_word):
    create_public_key()
    create_private_key()
    public_key_file = load_public_key()
    private_key_file = load_private_key()

    public_key = load_public_key()
    private_key = load_private_key()

    executed_word = ''
    if is_encryption:
        executed_word = private_key.encrypt(input_word.encode('utf-8'), Random.new().read)
    else:
        executed_word = private_key.decrypt(input_word)

    public_key_file.close()
    private_key_file.close()

    return executed_word
