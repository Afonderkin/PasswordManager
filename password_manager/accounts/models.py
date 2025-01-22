from django.db import models
from .utils import encrypt_password, decrypt_password


class Accounts(models.Model):
    """The model that stores user accounts"""
    email = models.EmailField(verbose_name='Email')
    encrypted_password = models.CharField(max_length=255, verbose_name='Encrypted Password')
    service_name = models.CharField(max_length=128, verbose_name='Service Name')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)

    @property
    def password(self):
        """Getter for password."""
        raise AttributeError("Password is not readable directly. Use `get_password` method.")

    @password.setter
    def password(self, password):
        """Setter for password."""
        self.encrypted_password = encrypt_password(password)

    def get_password(self, master_password):
        """Decrypted password if master password is correct."""
        if self.user.check_password(master_password):
            return decrypt_password(self.encrypted_password)
        raise ValueError("Incorrect master password.")

    def __str__(self):
        return f"{self.service_name} - {self.email}"

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
