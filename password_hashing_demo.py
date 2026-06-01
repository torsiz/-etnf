import hashlib
import bcrypt

# Sample password
password = "CyberSecure123!"

# --- SHA-256 Hashing Demo ---
sha256_hash = hashlib.sha256(password.encode()).hexdigest()
print(f"SHA-256 Hash: {sha256_hash}")

# --- bcrypt Hashing Demo ---
# bcrypt automatically adds salt, making hashes more secure
bcrypt_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(f"bcrypt Hash: {bcrypt_hash.decode()}")

# Verify bcrypt password
password_check = bcrypt.checkpw(password.encode(), bcrypt_hash)
print(f"Password Verified: {password_check}")
