class ValidationError(Exception):
    def __init__(self, **fields):
        self.fields = fields

    def __dict__(self):
        return self.fields
