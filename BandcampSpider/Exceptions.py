
class DomainError(Exception):
    def __init__(self, message="Not within the Bandcamp domain"):
        super().__init__(message)


class PageTypeException(Exception):
    def __init__(self, message="Wrong page type for this spider"):
        super().__init__(message)