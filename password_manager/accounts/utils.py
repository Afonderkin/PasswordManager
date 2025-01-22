from cryptography.fernet import Fernet


key = Fernet.generate_key()
cipher_suite = Fernet(key)


def encrypt_password(password):
    """ Encrypts a password using the cipher suite. """
    return cipher_suite.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password):
    """ Decrypts a password using the cipher suite. """
    return cipher_suite.decrypt(encrypted_password.encode()).decode()
