
class InvalidFormException(Exception):
    """Exception raised for errors in the input"""

    def __init__(self, message="Invalid payload structure"):
        super().__init__(message)