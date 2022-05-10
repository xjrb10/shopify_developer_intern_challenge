from jinja2 import Environment, FileSystemLoader
from sanic import Sanic, Request
from sanic.response import HTTPResponse

from db import InMemoryDB, Database
from model import Item
from routes import item

app = Sanic("shopify_developer_intern_challenge")
jinja_env = Environment(loader=FileSystemLoader("./templates"), enable_async=True)
InMemoryDB()  # init in-memory DB

app.blueprint(item)


async def render_template(request: Request, file_name: str, **kwargs):
    template = jinja_env.get_template(file_name)
    return await template.render_async({
        "app_name": app.name.replace("_", " ").title(),
        "request": request
    }, **kwargs)


@app.listener("after_server_start")
async def on_start(_app, loop):
    await Database.get_instance().add_item(Item(
        "Minty Shampoo", 32,
        "https://images.unsplash.com/photo-1546060432-b90a6441048f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&h=500&w=500&q=80"
    ))
    await Database.get_instance().add_item(Item(
        "Green Tea Bath Bomb", 32,
        "https://images.unsplash.com/photo-1614806687792-7fcec07dcbbd?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&h=500&w=500&q=80"
    ))
    await Database.get_instance().add_item(Item(
        "Rich Cream Lotion", 32,
        "https://images.unsplash.com/photo-1614859137322-20b54ff5d179?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&h=500&w=500&q=80"
    ))
    await Database.get_instance().add_item(Item(
        "Mineral Soap", 32,
        "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&h=500&w=500&q=80"
    ))
    await Database.get_instance().add_item(Item(
        "Wasabi Clay Mask (spicy)", 32,
        "https://images.unsplash.com/photo-1626783416763-67a92e5e7266?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&h=500&w=500&q=80"
    ))


@app.get('/')
async def index(request: Request) -> HTTPResponse:
    return HTTPResponse(await render_template(
        request, "index.html",
        items=dict([i async for i in Database.get_instance().list_items()]),
        deleted_items=[i async for i in Database.get_instance().list_deleted_items()],
    ))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
