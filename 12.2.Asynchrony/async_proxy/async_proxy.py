from aiohttp import web, ClientSession
from yarl import URL


async def proxy_handler(request: web.Request) -> web.Response:
    """
    Check request contains http url in query args:
        /fetch?url=http%3A%2F%2Fexample.com%2F
    and trying to fetch it and return body with http status.
    If url passed without scheme or is invalid raise 400 Bad request.
    On failure raise 502 Bad gateway.
    :param request: aiohttp.web.Request to handle
    :return: aiohttp.web.Response
    """
    session: ClientSession = request.app['session']

    url = request.query.get('url', None)
    if url is None:
        raise web.HTTPBadRequest(text='No url to fetch')

    url_scheme = URL(url).scheme
    if not url_scheme:
        raise web.HTTPBadRequest(text='Empty url scheme')
    if url_scheme not in ('http', 'https'):
        raise web.HTTPBadRequest(text=f'Bad url scheme: {url_scheme}')

    try:
        async with session.get(url) as response:
            content = await response.read()
            return web.Response(status=response.status, body=content)
    except Exception as e:
        raise web.HTTPBadGateway(text=f'Failed to fetch {url}, exception: {e}')


async def setup_application(app: web.Application) -> None:
    """
    Setup application routes and aiohttp session for fetching
    :param app: app to apply settings with
    """
    app['session'] = ClientSession()
    app.router.add_get('/fetch', proxy_handler)


async def teardown_application(app: web.Application) -> None:
    """
    Application with aiohttp session for tearing down
    :param app: app for tearing down
    """
    await app['session'].close()

