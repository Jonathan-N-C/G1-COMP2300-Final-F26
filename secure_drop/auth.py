# certificates and challenge signatures for mutual authentication
import os
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

CA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ca")

#the part of a certificate that the CA signs: email + public key
def _cert_body(email, public_key_pem):
    return json.dumps({"email": email, "public_key": public_key_pem}, sort_keys=True).encode()

#CA signs "this public key belongs to this email" (done at registration)
def create_certificate(email, public_key_pem):
    with open(os.path.join(CA_DIR, "ca_key.pem"), "r") as f:
        ca_key = RSA.import_key(f.read())
    signature = pss.new(ca_key).sign(SHA256.new(_cert_body(email, public_key_pem)))
    return {"email": email, "public_key": public_key_pem, "signature": base64.b64encode(signature).decode()}    

# check a certificate with the CA public key, returns the user's public key or None if fake
def verify_certificate(cert):
    try:
        with open(os.path.join(CA_DIR, "ca_pub.pem"), "r") as f:
            ca_pub = RSA.import_key(f.read())
        body = _cert_body(cert["email"], cert["public_key"])
        pss.new(ca_pub).verify(SHA256.new(body), base64.b64decode(cert["signature"]))
        return RSA.import_key(cert["public_key"])
    except (ValueError, KeyError, TypeError):
        return None    

#random challenge, new for every authentification so old answers can't be replayed
def new_nonce():
    return get_random_bytes(16)

#prove you own the private key by signing the challenge
def sign(priv_key, data):
    return pss.new(priv_key).sign(SHA256.new(data))

#check a signature with the other side's public key
def verify(pub_key, data, signature):
    try:
        pss.new(pub_key).verify(SHA256.new(data), signature)
        return True
    except (ValueError, TypeError):
        return False