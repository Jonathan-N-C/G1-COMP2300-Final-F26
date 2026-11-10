from Crypto.Cipher import AES, PKCS1_OAEP
from os import urandom

# encrypts file to send to an online mutual contact
def encryptFile(receiver, dataFile):
    # get recipient id_rsa.pub
    
    # decrypt id_rsa.pub
    
    # encrypt data with aes
    with open(dataFile, "r") as file:
        data = file.read()
    key = urandom(16)
    aes_enc = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = aes_enc.encrypt_and_digest(data)
    nonce = aes_enc.nonce

    # encrypt aes key with id_rsa.pub
    
    # send file in format: aes key -> encrypted data
    
    return
