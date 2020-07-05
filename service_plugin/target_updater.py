import asyncio
import threading
import time

import aiohttp
from aiohttp.client_exceptions import ClientConnectionError, ContentTypeError, ServerTimeoutError


class Target(object):
    def __init__(self, url):
        self._url = url
        self._status = None
        self._latency = 0

    @property
    def url(self):
        return self._url

    @property
    def status(self):
        return self._status

    @property
    def latency(self):
        return self._latency

    async def update(self):
        start_time = time.time()

        timeout = aiohttp.ClientTimeout(total=1)

        return_value = {
            "peer_target": self._url,
            "peer_id": "TIMEOUT"
        }

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(self._url + '/api/v1/status/peer', params={'channel': 'icon_dex'}) as response:
                    return_value = await response.json()
        except ClientConnectionError:
            # target peer is offline
            pass
        except (ServerTimeoutError, ContentTypeError):
            # target peer is faced jamming
            return_value["peer_id"] = "TIMEOUT"
        finally:
            self._status = return_value
            print(f"update {self._url} block_height({self._status['block_height']})")
        self._latency = time.time() - start_time

    def __repr__(self):
        return f"\n<Target: url({self._url}), latency({self.latency})>"

    def __lt__(self, other):
        if self.latency < other.latency:
            return True
        return False


class TargetUpdater(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self._conf = None
        self.targets = [Target('https://ctz.solidwallet.io')]
        self._loop = asyncio.new_event_loop()

    @property
    def relay_target(self):
        return self.targets[0].url

    @property
    def conf(self):
        return self._conf

    @conf.setter
    def conf(self, conf):
        self._conf = conf
        radiostations = self._conf['radiostations']
        targets = []
        for target in radiostations:
            targets.append(Target(target))

        self.targets = targets

    async def _update_targets(self):
        for target in self.targets:
            await target.update()

    def run(self):
        while True:
            print(f"target update...")
            print(f"targets({self.targets})")

            self._loop.run_until_complete(self._update_targets())

            self.targets.sort()
            time.sleep(5)
