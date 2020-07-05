#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

import gunicorn
import gunicorn.app.base
from earlgrey import asyncio
from iconcommons.icon_config import IconConfig
from iconcommons.logger import Logger
from iconrpcserver.default_conf.icon_rpcserver_config import default_rpcserver_config
from iconrpcserver.default_conf.icon_rpcserver_constant import ConfigKey
from iconrpcserver.icon_rpcserver_cli import ICON_RPCSERVER_CLI, ExitCode

from service_plugin.server_components import ServerComponents


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    """Web server runner by gunicorn.

    """

    def init(self, parser, opts, args):
        pass

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main():

    # Response server name as loopchain, not gunicorn.
    gunicorn.SERVER_SOFTWARE = 'loopchain'

    # Parse arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=str, dest=ConfigKey.PORT, default=None,
                        help="rest_proxy port")
    parser.add_argument("-c", type=str, dest=ConfigKey.CONFIG, default=None,
                        help="json configure file path")

    args = parser.parse_args()

    conf_path = args.config

    if conf_path is not None:
        if not IconConfig.valid_conf_path(conf_path):
            print(f'invalid config file : {conf_path}')
            sys.exit(ExitCode.COMMAND_IS_WRONG.value)
    if conf_path is None:
        conf_path = str()

    conf = IconConfig(conf_path, default_rpcserver_config)
    conf.load()
    conf.update_conf(dict(vars(args)))
    Logger.load_config(conf)

    _run_async(_run(conf))


def _run_async(async_func):
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(async_func)


def run_in_foreground(conf: 'IconConfig'):
    _run_async(_run(conf))


async def _run(conf: 'IconConfig'):
    Logger.print_config(conf, ICON_RPCSERVER_CLI)
    ServerComponents().conf = conf
    ServerComponents().set_resource()

    Logger.debug(f"Run gunicorn webserver for HA. Port = {conf[ConfigKey.PORT]}")

    # Configure SSL.
    ssl_context = ServerComponents().component.ssl_context
    certfile = ''
    keyfile = ''

    if ssl_context is not None:
        certfile = ssl_context[0]
        keyfile = ssl_context[1]

    options = conf.get(ConfigKey.GUNICORN_CONFIG, {})
    options.update({
        'bind': f'{conf[ConfigKey.HOST]}:{conf[ConfigKey.PORT]}',
        'certfile': certfile,
        'keyfile': keyfile,
        'SERVER_SOFTWARE': gunicorn.SERVER_SOFTWARE,
        'capture_output': False
    })

    # Launch gunicorn web server.
    ServerComponents().conf = conf
    # ServerComponents().ready()
    StandaloneApplication(ServerComponents().component.app, options).run()


# Run as gunicorn web server.
if __name__ == "__main__":
    main()
