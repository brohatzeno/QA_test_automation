class BaseTest:
    """Generic test skeleton with setup, execute, teardown."""

    registry = []

    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

    @classmethod
    def register(cls, test_cls):
        cls.registry.append(test_cls)
        return test_cls

    def setup(self):
        pass

    def execute(self):
        raise NotImplementedError("execute() must be implemented by the test")

    def teardown(self):
        pass

    def run(self):
        self.setup()
        try:
            return self.execute()
        finally:
            self.teardown()
