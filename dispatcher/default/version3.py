"""json rpc dispatcher version 3"""

import json

from iconcommons.logger import Logger
from iconrpcserver.default_conf.icon_rpcserver_constant import ConfigKey
from iconrpcserver.default_conf.icon_rpcserver_constant import DISPATCH_V3_TAG
from iconrpcserver.dispatcher import GenericJsonRpcServerError
from iconrpcserver.dispatcher import validate_jsonschema_v3
from iconrpcserver.utils.message_queue.stub_collection import StubCollection
from jsonrpcserver import async_dispatch
from jsonrpcserver.methods import Methods
from jsonrpcserver.response import DictResponse, ExceptionResponse
from sanic import response as sanic_response

methods = Methods()


class Version3Dispatcher:
    @staticmethod
    async def dispatch(request, channel_name=None):
        req_json = request.json
        url = request.url
        # channel = channel_name if channel_name is not None \
        #     else StubCollection().conf[ConfigKey.CHANNEL]

        context = {
            "url": url,
            "channel": 'icon_dex',
        }

        try:
            client_ip = request.remote_addr if request.remote_addr else request.ip
            Logger.info(f'rest_server_v3 request with {req_json}', DISPATCH_V3_TAG)
            Logger.info(f"{client_ip} requested {req_json} on {url}")

            validate_jsonschema_v3(request=req_json)
        except GenericJsonRpcServerError as e:
            response = ExceptionResponse(e, id=req_json.get('id', 0), debug=False)
        except Exception as e:
            response = ExceptionResponse(e, id=req_json.get('id', 0), debug=False)
        else:
            if "params" in req_json:
                req_json["params"]["context"] = context
            else:
                req_json["params"] = {"context": context}
            response: DictResponse = await async_dispatch(json.dumps(req_json), methods)
        Logger.info(f'rest_server_v3 with response {response}', DISPATCH_V3_TAG)
        return sanic_response.json(response.deserialized(), status=response.http_status, dumps=json.dumps)
