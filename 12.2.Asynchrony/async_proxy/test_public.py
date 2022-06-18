import asyncio
import time
from typing import Dict, Optional

import aiohttp
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop, make_mocked_request
from aiohttp import web
from yarl import URL

from .async_proxy import proxy_handler, setup_application, teardown_application


class FetchingTestCase(AioHTTPTestCase):
    async def get_application(self) -> web.Application:
        async def ok_handler(request: web.Request) -> web.Response:
            # https://docs.aiohttp.org/en/latest/web_exceptions.html
            raise web.HTTPOk(text='OK')

        async def fail_handler(request: web.Request) -> web.Response:
            raise web.HTTPInternalServerError(text='Internal server error')

        async def sleep_handler(request: web.Request) -> web.Response:
            await asyncio.sleep(1)
            raise web.HTTPOk(text='OK')

        test_app = web.Application()
        test_app.router.add_get('/ok', ok_handler)
        test_app.router.add_get('/fail', fail_handler)
        test_app.router.add_get('/sleep', sleep_handler)
        return test_app

    def server_address(self, path: str) -> str:
        return str(URL.build(
            scheme='http',
            host=self.server.host,
            port=self.server.port,
            path=path
        ))

    @staticmethod
    def fetch_url(url_to_fetch: str) -> str:
        return str(URL.build(
            path='/fetch',
            query={'url': url_to_fetch}
        ))

    @unittest_run_loop
    async def test_ok(self) -> None:
        async with aiohttp.ClientSession() as session:
            request = make_mocked_request(
                'GET', self.fetch_url(self.server_address('/ok'))
            )
            request.app['session'] = session  # One can use session inside handler
            try:
                response = await proxy_handler(request)
            except web.HTTPException as exc:
                response = exc
        assert response.body == b'OK'
        assert response.status == 200

    @unittest_run_loop
    async def test_fail(self) -> None:
        async with aiohttp.ClientSession() as session:
            request = make_mocked_request(
                'GET', self.fetch_url(self.server_address('/fail'))
            )
            request.app['session'] = session
            try:
                response = await proxy_handler(request)
            except web.HTTPException as exc:
                response = exc
        assert response.body == b'Internal server error'
        assert response.status == 500

    @unittest_run_loop
    async def test_bad_url(self) -> None:
        async with aiohttp.ClientSession() as session:
            request = make_mocked_request('GET', self.fetch_url('bad_url'))
            request.app['session'] = session
            try:
                response = await proxy_handler(request)
            except web.HTTPException as exc:
                response = exc
        assert response.status == 400
        assert response.body == b'Empty url scheme'

    @unittest_run_loop
    async def test_no_url(self) -> None:
        async with aiohttp.ClientSession() as session:
            request = make_mocked_request('GET', '/fetch')
            request.app['session'] = session
            try:
                response = await proxy_handler(request)
            except web.HTTPException as exc:
                response = exc
        assert response.status == 400
        assert response.body == b'No url to fetch'

    @unittest_run_loop
    async def test_bad_url_scheme(self) -> None:
        async with aiohttp.ClientSession() as session:
            request = make_mocked_request(
                'GET', self.fetch_url('ftp://example.com/')
            )
            request.app['session'] = session
            try:
                response = await proxy_handler(request)
            except web.HTTPException as exc:
                response = exc
        assert response.status == 400
        assert response.body == b'Bad url scheme: ftp'

    @unittest_run_loop
    async def test_concurrent(self) -> None:
        async with aiohttp.ClientSession() as session:
            tasks = []
            start = time.time()
            for _ in range(3):
                request = make_mocked_request(
                    'GET', self.fetch_url(self.server_address('/sleep'))
                )
                request.app['session'] = session
                tasks.append(proxy_handler(request))
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            end = time.time()
        assert end - start < 1.5
        assert all(response.status == 200 for response in responses)


class ApplicationTestCase(AioHTTPTestCase):
    async def get_application(self) -> web.Application:
        app = web.Application()
        await setup_application(app)

        async def test_handler(request: web.Request) -> web.Response:
            raise web.HTTPOk(text='pong')

        app.router.add_get('/ping', test_handler)  # For test purposes
        return app

    async def tearDownAsync(self) -> None:
        await teardown_application(self.server.app)

    def server_address(self, path: str, query: Optional[Dict[str, str]] = None) -> str:
        return str(URL.build(
            scheme='http',
            host=self.server.host,
            port=self.server.port,
            path=path,
            query=query
        ))

    async def fetch_url(
                self, session: aiohttp.ClientSession, url_to_fetch: str
            ) -> aiohttp.ClientResponse:
        url = str(URL(
            self.server_address(
                path='/fetch',
                query={'url': url_to_fetch}
            )
        ))

        return await session.get(url)

    @unittest_run_loop
    async def test_application(self) -> None:
        async with aiohttp.ClientSession() as session:
            response = await self.fetch_url(
                session, self.server_address(path='/ping')  # yep, server should fetching itself :)
            )
            assert response.status == 200
            assert await response.text() == 'pong'
            # Ensure application didn't close internal aiohttp session after first request
            response = await self.fetch_url(
                session, self.server_address(path='/ping')
            )
            assert response.status == 200
