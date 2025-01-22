import environ
from cryptography.fernet import Fernet
from password_manager.settings import env_file_path


env = environ.Env()
environ.Env.read_env(env_file=env_file_path)

key = env('FERNET_KEY').encode()

cipher_suite = Fernet(key)


def encrypt_password(password):
    """ Encrypts a password using the cipher suite. """
    return cipher_suite.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password):
    """ Decrypts a password using the cipher suite. """
    return cipher_suite.decrypt(encrypted_password.encode()).decode()
