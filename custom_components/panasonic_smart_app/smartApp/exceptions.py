class PanasonicBaseException(Exception):
    """ Base exception """


class PanasonicRefreshTokenNotFound(PanasonicBaseException):
    """ Refresh token not found """

    def __init__(
        self, message="Refresh token not existed. You may need to login again."
    ):
        super().__init__(message)
        self.message = message


class PanasonicTokenExpired(PanasonicBaseException):
    """ Token expired """


class PanasonicInvalidRefreshToken(PanasonicBaseException):
    """ Refresh token expired """


class PanasonicLoginFailed(PanasonicBaseException):
    """ Any other login exception """
