from base64url import Base64Url
from utils import base64url_decode
from encryption import HS256
import json

class JWT:
    """
    A class to handle JSON Web Token (JWT) creation and decoding.

    Attributes:
    header (str): A JSON string representing the JWT's header.
    payload (str): A JSON string representing the JWT's payload.
    _secret (str): A secret key used for signing the JWT.
    jwt (str): The encoded JWT string.

    Methods:
    encode(): Encodes the header, payload, and signs the JWT.
    decode(): Decodes the JWT and extracts the header and payload.
    """

    def __init__(self, header: dict, payload: dict, secret):
        """
        Initializes the JWT object with the header, payload, and secret.

        Parameters:
        header (dict): The header information for the JWT, typically containing the type and the signing algorithm.
        payload (dict): The payload of the JWT, containing the claims.
        secret (str): The secret key used for signing the JWT.
        """
        self.header = json.dumps(header)
        self.payload = json.dumps(payload)
        self._secret = secret
        self.jwt = None

    def encode(self):
        """
        Encodes the JWT by converting the header and payload to Base64Url format, 
        then creating a signature and constructing the full JWT token.

        Returns:
        str: The encoded JWT token.
        """
        # Convert header and payload into Base64Url
        base64Url_header = Base64Url(self.header).encode()
        base64Url_payload = Base64Url(self.payload).encode()

        # Create the message to be signed
        message = base64Url_header + "." + base64Url_payload

        # Create signature using HS256
        signature = HS256(message, self._secret).sign()

        # Construct JWT
        jwt_token = f"{base64Url_header}.{base64Url_payload}.{signature}"
        self.jwt = jwt_token

        return jwt_token
    
    def decode(self):
        """
        Decodes the JWT, extracting and returning the header and payload.

        Returns:
        tuple: A tuple containing the decoded header and payload.

        Raises:
        FileExistsError: If the JWT token does not exist or has not been created.
        """
        if self.jwt is None:
            raise FileExistsError("The JWT token does not exist. Remember to create it first.")
        
        # Splitting the JWT into its components
        header, payload, _ = self.jwt.split('.')

        # Decode the header and payload from Base64Url
        header = json.loads(base64url_decode(header))
        payload = json.loads(base64url_decode(payload))

        return header, payload