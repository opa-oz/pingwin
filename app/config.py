import os


class Config:
    org: str
    url: str
    bucket: str

    prod: bool

    username: str
    password: str

    def __init__(self):
        self.org = os.environ.get('INFLUXDB_ORG', 'homestation')
        self.url = os.environ.get('INFLUXDB_URL', 'http://192.168.0.64')
        self.bucket = os.environ.get('INFLUXDB_BUCKET', 'home')

        self.username = os.environ.get('INFLUXDB_USERNAME', 'admin')
        self.password = os.environ.get('INFLUXDB_PASSWORD', 'admin12345')

        self.prod = os.environ.get('PRODUCTION', 'false')


def get_config() -> Config:
    return Config()
