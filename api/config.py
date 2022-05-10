from collections import namedtuple

from environs import Env


class Config:
    _POSTGRES = namedtuple('postgres', 'dsn pool_max_size pool_min_size')

    def __init__(self):
        env = Env()
        env.read_env()

        self.postgres = self._POSTGRES(
            dsn=env.str('POSTGRES_DSN'),
            pool_max_size=env.int('POSTGRES_POOL_MAX_SIZE', 20),
            pool_min_size=env.int('POSTGRES_POOL_MIN_SIZE', 10),
        )


def init_config() -> Config:
    """ Function for getting configuration.

    :return:
    """
    return Config()
