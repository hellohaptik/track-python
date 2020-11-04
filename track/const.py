import enum

DEFAULT_HOST = 'https://api.interakt.ai'


class ApiPaths(enum.Enum):
    User = '/v1/public/track/users/'
    Event = '/v1/public/track/events/'
