from errors import UnsupportedDataTypeError
import pickle
import os

class Base64:
    """
    A class for encoding data into Base64 format.

    Attributes:
    - data: The input data to be encoded.
    - _binary_data: A private attribute to store the binary representation of the input data.
    - encoded_data: The Base64 encoded representation of the input data.

    Methods:
    - __init__(self, data): Initializes the Base64 object with the input data.
    - encode(self): Encodes the input data into Base64 format.
    """

    BASE64_TABLE = {
        0: 'A',  1: 'B',  2: 'C',  3: 'D',  4: 'E',  5: 'F',  6: 'G',  7: 'H',
        8: 'I',  9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P',
        16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X',
        24: 'Y', 25: 'Z', 26: 'a', 27: 'b', 28: 'c', 29: 'd', 30: 'e', 31: 'f',
        32: 'g', 33: 'h', 34: 'i', 35: 'j', 36: 'k', 37: 'l', 38: 'm', 39: 'n',
        40: 'o', 41: 'p', 42: 'q', 43: 'r', 44: 's', 45: 't', 46: 'u', 47: 'v',
        48: 'w', 49: 'x', 50: 'y', 51: 'z', 52: '0', 53: '1', 54: '2', 55: '3',
        56: '4', 57: '5', 58: '6', 59: '7', 60: '8', 61: '9', 62: '+', 63: '/'
    }

    def __init__(self, data):
        """
        Initializes the Base64 object with the given data.

        Parameters:
        - data (str, bytes, int, or dict): The input data to be encoded. Supported data types are string, bytes, integer, and dictionary.
        """
        self.data = data
        self._binary_data = ""
        self.encoded_data = ""

    def _to_binary(self):
        """
        Convert data of various types to binary representation.

        Parameters:
        data (int, str, bytes, list, or custom object): The input data to be converted.

        Returns:
        str, bytes, list, or bytes: The binary representation of the input data.

        Raises:
        UnsupportedDataTypeError: If the input data type is not supported.

        Supported Data Types:
        - Integer: Converts an integer to its binary representation.
        - String: Converts each character in the string to ASCII binary.
        - Bytes: Returns bytes as is (no conversion).
        - Custom Object (with '__dict__' attribute): Serializes the object
        """
        res = None
        data = self.data

        if isinstance(data, int):
            # Convert integers to binary
            res = bin(data)[2:]
        elif isinstance(data, str) and os.path.isfile(data):
            # Convert fiels to binary
            with open(data, 'rb') as file:
                binary_data = file.read()
            res = ''.join(format(byte, '08b') for byte in binary_data)
        elif isinstance(data, str):
            # Convert string to binary
            binary_representation = ''.join(format(ord(char), '08b') for char in data)
            res = binary_representation
        elif isinstance(data, bytes):
            res = ''.join(format(byte, '08b') for byte in data)
        elif isinstance(data, dict):
            # Convert custom objects to binary
            bytes_data = pickle.dumps(data)
            res = ''.join(format(byte, '08b') for byte in bytes_data)
        else:
            raise UnsupportedDataTypeError(f"Unsupported data type: {type(data)}")

        return res

    def _pad_binary_data(self):
        """Pads the binary data to make its langth a multiple of 6."""
        padding_length = 6 - (len(self.binary_data) % 6)
        if padding_length != 6:
            self.binary_data += '0' * padding_length

    def _split_into_chunks(self, group_size: int = 6):
        """
        Splits the binary data into chunks of the specified group size.

        Parameters:
        - group_size (int): The size of each chunk. Default is 6 bits.

        Returns:
        - list of str: List of binary string chunks.
        """
        return [self.binary_data[i:i + group_size] for i in range(0, len(self.binary_data), group_size)]
    
    def _map_to_base64(self, chunks):
        """
        Maps each binary chunk to its corresponding Base64 character.

        Parameters:
        - chunks (list of str): Binary string chunks.

        Returns:
        - str: Base64 encoded string.
        """
        return ''.join(self.BASE64_TABLE[int(chunk, 2)] for chunk in chunks)
    
    def encode(self):
        """
        Encodes the input data into Base64 format.

        Returns:
        - str: Base64 encoded string of the input data.
        """
        self.binary_data = self._to_binary()
        self._pad_binary_data()
        chunks = self._split_into_chunks()
        self.encoded_data = self._map_to_base64(chunks)
        return self.encoded_data
    

class Base64Url(Base64):
    """
    A class for encoding data into Base64Url format, inheriting from Base64 class.
    Base64Url format is URL-safe, making it suitable for use in URLs and file names.

    Methods:
    - __init__(self, data): Inherits the constructor from Base64 class.
    - encode(self): Encodes the input data into Base64Url format.
    """

    def _map_to_base64url(self, chunks):
        """
        Maps each binary chunk to its corresponding Base64Url character.

        Parameters:
        - chunks (list of str): Binary string chunks.

        Returns:
        - str: Base64Url encoded string.
        """
        base64_encoded = super()._map_to_base64(chunks)

        # Replace '+' with '-', '/' with '_' and remove padding
        base64url_encoded = base64_encoded.replace('+', '-').replace('/', '_').rstrip('=')
        return base64url_encoded

    def encode(self):
        """
        Encodes the input data into Base64Url format by altering the standard Base64 encoding to be URL-safe.

        Returns:
        - str: Base64Url encoded string of the input data.
        """
        self.binary_data = self._to_binary()
        self._pad_binary_data()
        chunks = self._split_into_chunks()
        self.encoded_data = self._map_to_base64url(chunks)
        return self.encoded_data