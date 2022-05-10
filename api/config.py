from collections import namedtuple

from environs import Env


class Config:
    _POSTGRES = namedtuple('postgres', 'dsn pool_max_size pool_min_size')

    def __init__(self):
        env = Env()
        env.read_env()

        self.postgres = self._POSTGRES(
            dsn=env.str('POSTGRES_DSN'),
            pool_max_size=env.int('POSTGRES_POOL_MAX_SIZE'),
            pool_min_size=env.int('POSTGRES_POOL_MIN_SIZE'),
        )
        self.max_codes_per_request = env.int('MAX_CODES_PER_REQUEST')


def init_config() -> Config:
    """ Function for getting configuration.

    :return:
    """
    return Config()
