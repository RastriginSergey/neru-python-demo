import json
import sys
sys.path.append("vendor")

import os
from datetime import datetime

from aiohttp import web

async def handle(request):
    body = {
        "hello": "world",
        "time": str(datetime.now())
    }
    print(f"Received req @ {body['time']}")
    return web.Response(text=json.dumps(body), status=200)

app = web.Application()
app.add_routes([
    web.route("*", "/{path:.*}", handle),
])

if __name__ == "__main__":
    port = int(os.getenv("NERU_APP_PORT", "3000"))
    web.run_app(app, host="0.0.0.0", port=port)