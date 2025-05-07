from aiohttp import web
import aiosqlite
import os
from aiohttp_cors import setup as cors_setup, ResourceOptions, CorsViewMixin

# Get port from environment variable or use default
PORT = int(os.getenv('PORT', 8000))

async def get_links(request):
    async with aiosqlite.connect('links.db') as db:
        async with db.execute('SELECT id, url FROM links') as cursor:
            links = await cursor.fetchall()
    
    return web.json_response([{'id': id, 'url': url} for id, url in links])

async def serve_index(request):
    return web.FileResponse('./webapp/index.html')

async def serve_static(request):
    file_path = f'./webapp/{request.match_info["path"]}'
    if os.path.exists(file_path):
        return web.FileResponse(file_path)
    return web.Response(status=404)

app = web.Application()
# Setup CORS
cors = cors_setup(app, defaults={
    "*": ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
        allow_methods="*"
    )
})

# Add routes
app.router.add_get('/api/links', get_links)
app.router.add_get('/', serve_index)
app.router.add_get('/{path:.*}', serve_static)

# Configure CORS for all routes
for route in list(app.router.routes()):
    cors.add(route)

if __name__ == '__main__':
    web.run_app(app, port=PORT, host='0.0.0.0') 