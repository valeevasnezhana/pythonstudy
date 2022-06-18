import asyncio
import time
from functools import partial

import aiohttp
import requests
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web

from .sync_vs_async import async_fetch, sync_fetch, async_requests, threaded_requests


class FetchingTestCase(AioHTTPTestCase):
    async def get_application(self) -> web.Application:
        async def hello_handler(request: web.Request) -> web.Response:
            return web.Response(text='Hello, asyncio!')

        app = web.Application()
        app.router.add_get('/', hello_handler)
        return app

    @property
    def server_address(self) -> str:
        return f'http://{self.server.host}:{self.server.port}/'

    @unittest_run_loop
    async def test_async_fetching(self) -> None:
        async with aiohttp.ClientSession() as session:
            response = await async_fetch(session, self.server_address)
        assert response == 'Hello, asyncio!'

    @unittest_run_loop
    async def test_sync_fetching(self) -> None:
        loop = asyncio.get_running_loop()
        with requests.Session() as session:
            response = await loop.run_in_executor(  # a convenient way to wait for a syncronous code
                None,  # default ThreadPoolExecuter
                partial(sync_fetch, session, self.server_address)
            )
        assert response == 'Hello, asyncio!'


class TimedTestCase(AioHTTPTestCase):
    async def get_application(self) -> web.Application:
        async def sleepy_handler(request: web.Request) -> web.Response:
            await asyncio.sleep(1)
            return web.Response(text='OK')

        app = web.Application()
        app.router.add_get('/', sleepy_handler)
        return app

    @property
    def server_address(self) -> str:
        return f'http://{self.server.host}:{self.server.port}/'

    @unittest_run_loop
    async def test_async_parallel(self) -> None:
        start = time.time()
        responses = await async_requests(
            [self.server_address] * 10
        )
        end = time.time()
        assert end - start <= 1.5
        assert responses == ['OK'] * 10

    @unittest_run_loop
    async def test_threaded_parallel(self) -> None:
        loop = asyncio.get_running_loop()
        start = time.time()
        responses = await loop.run_in_executor(
            None,
            partial(threaded_requests, [self.server_address] * 10)
        )
        end = time.time()
        assert end - start <= 1.5
        assert responses == ['OK'] * 10
