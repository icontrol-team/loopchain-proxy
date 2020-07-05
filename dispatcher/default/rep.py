"""json rpc dispatcher version 3"""

from iconcommons.logger import Logger

from dispatcher.default import methods
from iconrpcserver.utils.icon_service import response_to_json_query, RequestParamType
from iconrpcserver.utils.icon_service.converter import convert_params
from iconrpcserver.utils.json_rpc import get_channel_stub_by_channel_name


class RepDispatcher:
    @staticmethod
    @methods.add
    async def rep_getListByHash(**kwargs):
        channel = kwargs['context']['channel']
        channel_stub = get_channel_stub_by_channel_name(channel)
        request = convert_params(kwargs, RequestParamType.get_reps_by_hash)
        reps_hash = request.get('repsHash')
        reps = await channel_stub.async_task().get_reps_by_hash(reps_hash=reps_hash)
        Logger.debug(f"reps_hash: {reps_hash}, reps: {reps}")
        response = [{'address': rep['id'], 'p2pEndpoint': rep['p2pEndpoint']} for rep in reps]

        return response_to_json_query(response)
