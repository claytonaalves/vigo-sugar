class CustomException(Exception):

    def __init__(self, message, code):
        Exception.__init__(self, message)
        self.code = code

class DeleteError(CustomException):
    pass

class RequiredFieldsError(CustomException):
    pass

class DatabaseError(CustomException):
    pass

