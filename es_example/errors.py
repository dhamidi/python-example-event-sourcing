class ValidationError(Exception):
    def __init__(self, **fields):
        self.fields = fields
