class UnsupportedDataTypeError(Exception):
    """Exception raised for errors in the input data type.

    Attributes:
        data_type -- data type of the input which caused the error
        message -- explanation of the error
    """

    def __init__(self, data_type, message="Unsupported data type provided"):
        self.data_type = data_type
        self.message = message
        super().__init__(f"{self.message}: {self.data_type}")

    def __str__(self):
        return f"{self.message} --> {self.data_type}"
