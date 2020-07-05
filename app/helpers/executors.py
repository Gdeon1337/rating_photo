import asyncio
from typing import Optional, List

from ddtrace import tracer
from ddtrace.context import Context


def _warp_trace_context(context: Context, func, *args):
    tracer.context_provider.activate(context)
    return func(*args)


async def _async_warp_trace_context(context: Context, func, *args):
    tracer.context_provider.activate(context)
    return await func(*args)


async def _async_warp_coro_trace_context(context: Context, coro):
    tracer.context_provider.activate(context)
    return await coro


def current_context() -> Optional[Context]:
    span = tracer.current_span()
    if span:
        return span.context.clone()
    return None


def run_in_executor(func, *args, context: Optional[Context] = None, loop: Optional[asyncio.AbstractEventLoop] = None):
    context = context or current_context()
    loop = loop or asyncio.get_event_loop()
    return loop.run_in_executor(None, _warp_trace_context, context, func, *args)


def create_task(coro, context: Optional[Context] = None, loop: Optional[asyncio.AbstractEventLoop] = None):
    context = context or current_context()
    loop = loop or asyncio.get_event_loop()
    return loop.create_task(_async_warp_coro_trace_context(context, coro))


def gather(func, items: List, expand: bool = False, context: Optional[Context] = None):
    context = context or current_context()
    if expand:
        return asyncio.gather(*[_async_warp_trace_context(context, func, *item) for item in items])
    return asyncio.gather(*[_async_warp_trace_context(context, func, item) for item in items])
