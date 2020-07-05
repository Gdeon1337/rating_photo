from typing import Dict

from sanic_openapi import doc  # pylint: disable=wrong-import-order


def form_data_consumes(*args, **kwargs):
    return doc.consumes(
        *args,
        **kwargs,
        content_type='multipart/form-data',
        location='formData'
    )


def json_consumes(json_body: Dict, *args, **kwargs):
    return doc.consumes(
        doc.JsonBody(json_body),
        *args,
        **kwargs,
        content_type='application/json',
        location='body'
    )


def error_response(code: int, response: str):
    return doc.response(
        code,
        {'response': doc.String(response)},
        description=response
    )
