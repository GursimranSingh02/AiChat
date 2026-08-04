import hashlib
import hmac
import os

ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 260000
SALT_BYTES = 16
HASH_BYTES = 32


def hash_password(password: str) -> str:
    salt = os.urandom(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS,
        dklen=HASH_BYTES,
    )
    return f"{ALGORITHM}${ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = hashed_password.split("$", 3)
        if algorithm != ALGORITHM:
            return False

        candidate = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations),
            dklen=len(bytes.fromhex(digest_hex)),
        ).hex()
        return hmac.compare_digest(candidate, digest_hex)
    except (ValueError, TypeError):
        return False
