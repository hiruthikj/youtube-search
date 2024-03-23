import logging
from collections.abc import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse

from ..common.utils import get_printable


def log_response(req_body, res_body):
    logging.info(f"Request: {get_printable(req_body)}. Response: {res_body}")


class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            req_body = await request.body()
            logging.info(f"Recieved Request on {request.url}. Request Details: {get_printable(request)}")

            response = await original_route_handler(request)

            if isinstance(response, StreamingResponse):
                res_body = b''
                async for item in response.body_iterator:
                    res_body += item

                task = BackgroundTask(log_response, req_body, res_body)
                return Response(content=res_body, status_code=response.status_code,
                        headers=dict(response.headers), media_type=response.media_type, background=task)
            else:
                res_body = response.body
                response.background = BackgroundTask(log_response, req_body, res_body)
                return response

        return custom_route_handler
