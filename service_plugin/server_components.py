from iconrpcserver.server.rest_server import ServerComponents as BaseServerComponents
from iconrpcserver.components import SingletonMetaClass
from service_plugin.target_updater import TargetUpdater


class ServerComponents(metaclass=SingletonMetaClass):
    def __init__(self):
        self._servercomponent = BaseServerComponents
        self.target_updater = TargetUpdater()
        self.target_updater.start()

    @property
    def component(self):
        return self._servercomponent()

    @property
    def conf(self):
        return self._servercomponent.conf

    @conf.setter
    def conf(self, conf):
        self._servercomponent.conf = conf
        self.target_updater.conf = conf

    def set_resource(self):
        from dispatcher.default import Version3Dispatcher
        app = self._servercomponent().app
        app.add_route(Version3Dispatcher.dispatch, '/api/v3/<channel_name>', methods=['POST'])
        app.add_route(Version3Dispatcher.dispatch, '/api/v3/', methods=['POST'])
