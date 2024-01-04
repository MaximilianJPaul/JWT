import hashlib

class HS256:
    """
    HS256 class for creating a message authentication code using a secret key and SHA-256.

    Attributes:
    message (str): The message to be authenticated.
    _message_bytes (bytes): Byte representation of the message.
    _secret_key (bytes): The secret key used for hashing.
    _block_size (int): The block size of the hash function (SHA-256), in bytes.
    _ipad (bytes): The inner padding.
    _opad (bytes): The outer padding.
    """

    def __init__(self, message, secret_key):
        """
        Initializes the HS256 object with a message and a secret key.

        Parameters:
        message (str): The message to be authenticated.
        secret_key (bytes): The secret key used for hashing.
        """
        self.message = message
        self._message_bytes = message.encode('utf-8')
        self._secret_key = secret_key
        self._block_size = 64  # Block size of SHA-256 in bytes
        self._ipad = bytes([0x36] * self._block_size)  # Inner padding
        self._opad = bytes([0x5C] * self._block_size)  # Outer padding

    def preprocess_key(self):
        """
        Preprocesses the secret key to ensure it matches the block size.
        Hashes the key if it is longer than the block size.
        Pads the key with zeros if it is shorter than the block size.
        """
        if len(self._secret_key) > self._block_size:
            # Hash key with SHA-256 if it's longer than block size
            hasher = hashlib.sha256()
            hasher.update(self._secret_key)
            self._secret_key = hasher.digest()
        elif len(self._secret_key) < self._block_size:
            # Pad key with zeros if it's shorter than block size
            self._secret_key += bytes([0x00] * (self._block_size - len(self._secret_key)))

    def sign(self):
        """
        Generates the HS256 signature of the message using SHA-256.

        Returns:
        str: The HS256 signature in hexadecimal format.
        """
        # Preprocess the key to ensure proper length
        self.preprocess_key()

        # Create inner and outer padded keys
        inner_padded_key = bytes(x ^ y for x, y in zip(self._secret_key, self._ipad))
        outer_padded_key = bytes(x ^ y for x, y in zip(self._secret_key, self._opad))

        # Compute inner hash
        inner_hash = hashlib.sha256(inner_padded_key + self._message_bytes).digest()
        # Compute outer hash
        outer_hash = hashlib.sha256(outer_padded_key + inner_hash).hexdigest()

        return outer_hash