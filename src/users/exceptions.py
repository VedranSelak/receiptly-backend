from fastapi import HTTPException


class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        self.detail = "User with this email already exists!"
        self.status_code = 400


class UserNotFoundException(HTTPException):
    def __init__(self):
        self.detail = "User with this email doesn't exists!"
        self.status_code = 404


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        self.detail = "Invalid user credentials!"
        self.status_code = 404
