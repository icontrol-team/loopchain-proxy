"""json rpc dispatcher version 3"""

from typing import Any, Optional

from dispatcher.default import methods
from iconcommons.logger import Logger
from iconrpcserver.utils.icon_service import response_to_json_query
from iconrpcserver.utils.icon_service.converter import make_request
from iconrpcserver.utils.json_rpc import get_icon_stub_by_channel_name


class IseDispatcher:
    HASH_KEY_DICT = ['hash', 'blockHash', 'txHash', 'prevBlockHash']

    @staticmethod
    @methods.add
    async def ise_getStatus(**kwargs):
        Logger.warning(f'Hello World2')
        # channel = kwargs['context']['channel']
        # method = 'ise_getStatus'
        # request = make_request(method, kwargs)
        # score_stub = get_icon_stub_by_channel_name(channel)
        # response = await score_stub.async_task().query(request)
        # error = response.get('error')
        # if error is None:
        #     IseDispatcher._hash_convert(None, response)
        response = {'hello': 'world'}
        return response_to_json_query(response)

    @staticmethod
    def _hash_convert(key: Optional[str], response: Any):
        if key is None:
            result = response
        else:
            result = response[key]
        if isinstance(result, dict):
            for key in result:
                IseDispatcher._hash_convert(key, result)
        elif key in IseDispatcher.HASH_KEY_DICT:
            if isinstance(result, str):
                if not result.startswith('0x'):
                    response[key] = f'0x{result}'
