import os
from aiohttp import web, ClientSession
import urllib


routes = web.RouteTableDef()
BASE_URL = os.environ.get('API_HOST')
IMAGE_URL = os.environ.get('QR_HOST')

@routes.get('/')
async def hello(request):
    try:
        words = int(request.query.get('words', 5))
    except ValueError:
        return web.Response(text='words should be numeric', status=400)
    async with ClientSession() as session:
        url = '/'.join([BASE_URL, 'api', 'lorem', 'h1', f'{words -1}-{words +1}']) 
        async with session.get(f'http://{url}') as resp:
            result = await resp.json()
    text = urllib.parse.quote(result['text_out'].strip('</h1>'))
    async with ClientSession() as session:
        url = '/'.join([IMAGE_URL, 'api', 'v1', f'?{text}', '']) 
        async with session.get(f'http://{url}') as resp:
            return web.Response(body=await resp.content.read(), 
                                headers={'Content-Type': resp.headers['Content-Type']})


app = web.Application()
app.add_routes(routes)
web.run_app(app)
