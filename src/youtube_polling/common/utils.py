from starlette.requests import Request


def get_request_repr(request_obj: Request):
    headers = dict(request_obj.headers)
    # TODO: Better Log Obfuscation
    if "authorization" in headers.keys():
        headers["authorization"] = "********"

    request_dict = {
        "method": request_obj.method,
        "url": str(request_obj.url),
        "headers": headers,
        "query_params": dict(request_obj.query_params),
        "path_params": request_obj.path_params,
        "client": request_obj.client,
        "body": request_obj._body,
        # "cookies": request_obj.cookies,
    }
    str_repr = str(request_dict)
    return str_repr


def get_printable(input):
    if isinstance(input, Request):
        return get_request_repr(input)

    return str(input)


def convert_pydantic_error(errors: list):
    return [
        {"check": loc, "error": error["msg"]}
        for error in errors
        for loc in error["loc"]
    ]
