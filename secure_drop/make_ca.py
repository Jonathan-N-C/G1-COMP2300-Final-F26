#creates the test CA (run once): a key pair that signs user certificates
import os
from Crypto.PublicKey import RSA

CA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ca")
os.makedirs(CA_DIR, exist_ok=True)

ca_key = RSA.generate(2048)

# CA private key: signs certificates, keep it secret
with open(os.path.join(CA_DIR, "ca_key.pem"), "w") as f:
    f.write(ca_key.export_key().decode())
os.chmod(os.path.join(CA_DIR, "ca_key.pem"), 0o600)

#CA  public key: every client uses it to verify certificates
with open(os.path.join(CA_DIR, "ca_pub.pem"), "w") as f:
    f.write(ca_key.public_key().export_key().decode())

print("CA created in", CA_DIR)    