import asyncio
from typing import List, Optional

from ddtrace import tracer
from ddtrace.context import Context
from ddtrace.propagation.http import HTTPPropagator
from sanic.request import Request
from sanic.response import BaseHTTPResponse


_ddtrace_propagator = HTTPPropagator()


async def ddtarce_on_request(request: Request):
    context = _ddtrace_propagator.extract(request.headers)
    tracer.context_provider.activate(context)
    *_, match_info, endpoint = request.app.router.get(request)
    ddtarce_span = tracer.trace('sanic.request', request.app.config.SERVICE_NAME, endpoint, 'web')
    ddtarce_span.set_tag('http.version', request.version)
    ddtarce_span.set_tag('http.method', request.method)
    ddtarce_span.set_tag('http.match_info', match_info)
    ddtarce_span.set_tag('http.headers', dict(request.headers))
    request['ddtarce_span'] = ddtarce_span


async def ddtarce_on_response(request: Request, response: BaseHTTPResponse):
    ddtarce_span = request.get('ddtarce_span')
    if ddtarce_span:
        ddtarce_span.set_tag('http.status_code', response.status)
        ddtarce_span.finish()


def current_context() -> Optional[Context]:
    span = tracer.current_span()
    if span:
        return span.context.clone()
    return None


def _warp_trace_context(context: Context, func, *args):
    tracer.context_provider.activate(context)
    return func(*args)


def run_in_executor(func, *args, context: Optional[Context] = None, loop: Optional[asyncio.AbstractEventLoop] = None):
    context = context or current_context()
    loop = loop or asyncio.get_event_loop()
    return loop.run_in_executor(None, _warp_trace_context, context, func, *args)


def gather_in_executor(
    func,
    items: List,
    expand: bool = False,
    context: Optional[Context] = None,
    loop: Optional[asyncio.AbstractEventLoop] = None
):
    context = context or current_context()
    loop = loop or asyncio.get_event_loop()
    if expand:
        return asyncio.gather(*[run_in_executor(func, *item, context=context, loop=loop) for item in items])
    return asyncio.gather(*[run_in_executor(func, item, context=context, loop=loop) for item in items])


async def _async_warp_trace_context(context: Context, func, *args):
    tracer.context_provider.activate(context)
    return await func(*args)


def gather(func, items: List, expand: bool = False, context: Optional[Context] = None):
    context = context or current_context()
    if expand:
        return asyncio.gather(*[_async_warp_trace_context(context, func, *item) for item in items])
    return asyncio.gather(*[_async_warp_trace_context(context, func, item) for item in items])


async def _async_warp_coro_trace_context(context: Context, coro):
    tracer.context_provider.activate(context)
    return await coro


def create_task(coro, context: Optional[Context] = None, loop: Optional[asyncio.AbstractEventLoop] = None):
    context = context or current_context()
    loop = loop or asyncio.get_event_loop()
    return loop.create_task(_async_warp_coro_trace_context(context, coro))
