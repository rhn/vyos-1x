from dhcp_server import *

import vyos
from vyos import ConfigError
from vyos.config import Config

# Monkey patch verification, current system state should not matter, but rather the intended system state (from config files).
def is_subnet_connected(subnet, primary=False):
    return True

vyos.validate.is_subnet_connected = is_subnet_connected


class TestConfig(vyos.config.BaseConfig):
    def __init__(self, config_file):
        super().__init__()
        with open(config_file) as f:
            running_config_text = f.read()
        self._config_tree = vyos.configtree.ConfigTree(running_config_text)

    def exists(self, path):
        return self._exists(self._config_tree, path)

    def list_nodes(self, path, default=[]):
        return self._list_nodes(self._config_tree, path, default)

    def return_value(self, path, default=None):
        return self._return_value(self._config_tree, path, default)

    def return_values(self, path, default=None):
        return self._return_values(self._config_tree, path, default)


if __name__ == '__main__':
    try:
        config_file='./config.boot.default'
        c = get_config(TestConfig(config_file))
        verify(c)
        generate(c, prefix='./')
    except ConfigError as e:
        print(e)
        sys.exit(1)
