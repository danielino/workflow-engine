class BootstrapException(Exception):
    pass


class PluginNotFoundException(BootstrapException):
    pass


class StepsNotFoundException(BootstrapException):
    pass
