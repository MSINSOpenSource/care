from cryptography.fernet import Fernet, MultiFernet
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.encoding import force_bytes, force_text


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import base64


class FernetEncryption:
    @cached_property
    def keys(self):
        keys = getattr(settings, 'FERNET_KEYS', None)
        if keys is None:
            keys = [settings.SECRET_KEY]
        return keys

    @cached_property
    def fernet_keys(self):
        if getattr(settings, 'FERNET_USE_HKDF', True):
            return [self.derive_fernet_key(k) for k in self.keys]
        return self.keys

    @cached_property
    def fernet(self):
        if len(self.fernet_keys) == 1:
            return Fernet(self.fernet_keys[0])
        return MultiFernet([Fernet(k) for k in self.fernet_keys])

    def encrypt(self, value, connection):
        if value is not None:
            retval = self.fernet.encrypt(force_bytes(value))
            return connection.Database.Binary(retval)

    def decrypt(self, value):
        value = bytes(value)
        return force_text(self.fernet.decrypt(value))

    def derive_fernet_key(self, input_key):
        backend = default_backend()
        info = b'django-fernet-fields'
        # We need reproducible key derivation, so we can't use a random salt
        salt = b'django-fernet-fields-hkdf-salt'

        """Derive a 32-bit b64-encoded Fernet key from arbitrary input key."""
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            info=info,
            backend=backend,
        )
        return base64.urlsafe_b64encode(hkdf.derive(force_bytes(input_key)))
