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


class PanasonicDeviceOffline(PanasonicBaseException):
    """ Target device is offline """

    def __init__(
        self, message="Device is offline. Retry later..."
    ):
        super().__init__(message)
        self.message = message
