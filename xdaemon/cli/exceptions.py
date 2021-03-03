class JobAlreadyExists(Exception):

    def __init__(self, name):
        self.name = name


class PermissionError(Exception):

    def __init__(self, message):
        self.message = message
